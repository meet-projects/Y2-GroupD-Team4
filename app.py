from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

Config = {
  "apiKey": "AIzaSyC-hCpbDNBYMPbZe73ONWraehZjzig7PxM",
  "authDomain": "nefashoty2.firebaseapp.com",
  "databaseURL": "https://nefashoty2-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "nefashoty2",
  "storageBucket": "nefashoty2.appspot.com",
  "messagingSenderId": "29434455725",
  "appId": "1:29434455725:web:53dd13f83be0e104a84824"}
fb = pyrebase.initialize_app(Config)
auth = fb.auth()
db = fb.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'loai'

#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('home'))
        # except:
        #     print('Auth login Failed')
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['full_name']
        # 
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        login_session['user']['name'] = name
        try:
            
            # print("vadim1")
            user = {'email': email, 'password' : password, 'full name': name}
            UID = login_session['user']['localId']
            db.child('Users').child(UID).set(user)
            return redirect(url_for('home'))
        except:
            print('signup failed')

    return render_template("signin.html")


@app.route('/home', methods=['GET', "POST"])
def home():
    return render_template('home.html')
#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)