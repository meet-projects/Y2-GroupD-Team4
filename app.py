from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import os 

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


UPLOAD_FOLDER='static/uploads'
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@nefashot.com' and password == 'admin123':
            return redirect(url_for('admin'))
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            print('Auth login Failed')
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['full_name']
        
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        login_session['user']['name'] = name
        try:
            
            # print("vadim1")
            user = {'email': email, 'password' : password, 'full_name': name}
            UID = login_session['user']['localId']
            db.child('Users').child(UID).set(user)
            return redirect(url_for('home'))
        except:
            print('signup failed')

    return render_template("signin.html")


@app.route('/home', methods=['GET', "POST"])
def home():

    uid = login_session['user']['localId']
    name = db.child('Users').child(uid).child('full_name').get().val()
    return render_template('home.html', n = name)
#Code goes above here

# db.set('Applicants')
# db.child('Applicants').push({'name': 'Sergey Auslender','age':16 , 'exp': 'Robotics mentor'})
# db.child('Applicants').push({'name': 'Yosi Cohen','age':25 , 'exp': 'DJ for hire, pianist'})

@app.route('/events', methods = ['GET', 'POST'])
def events():
    uid = login_session['user']['localId']
    name = db.child('Users').child(uid).child('full_name').get().val()
    dicti = db.child('Events').get().val()
    return render_template('events.html', d = dicti, n = name)


@app.route('/upload', methods = ['GET', 'POST'])
def upload():
  if request.method == "POST":
    name=request.form['name']
    price=request.form['price']
    image=request.form['image']
    discrption=request.form['discrption']
    # filename=image.filename
    # UPLOAD_FOLDER=os.path.join('static', 'uploads')
    # if not os.path.exists(UPLOAD_FOLDER):
    #   os.makedirs(UPLOAD_FOLDER)
    # image_filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # image.save(image_filename)
    post={"name":name,"price":price,"image":image,"discrption":discrption}
    db.child("Posts").push(post)
    return redirect(url_for('shop'))
  else:
    return render_template('upload.html')


@app.route('/apply', methods = ['GET', 'POST'])
def apply():
    if request.method == 'POST':
        nam = request.form['full_name']
        age = request.form['age']
        exp = request.form['exp']
        dictin = {'name': nam,'age': age , 'exp': exp}
        db.child('Applicants').push(dictin)
        return redirect(url_for('home'))
    uid = login_session['user']['localId']
    name = db.child('Users').child(uid).child('full_name').get().val()
    return render_template('help.html', n = name)

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    dictio = db.child('Applicants').get().val()
    return render_template('admin.html', d = dictio)



@app.route('/shop', methods = ['GET', 'POST'])
def shop():
  posts=db.child('Posts').get().val()
  if posts != None:
    return render_template('shop.html',posts=posts)
  else:
    return render_template('shop.html',posts=None)





if __name__ == '__main__':
    app.run(debug=True)