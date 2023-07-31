from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

Config = {
  "apiKey": "AIzaSyC-hCpbDNBYMPbZe73ONWraehZjzig7PxM",
  "authDomain": "nefashoty2.firebaseapp.com",
  "projectId": "nefashoty2",
  "storageBucket": "nefashoty2.appspot.com",
  "messagingSenderId": "29434455725",
  "appId": "1:29434455725:web:53dd13f83be0e104a84824",
  "databaseURL": "https://nefashoty2-default-rtdb.europe-west1.firebasedatabase.app/"}
fb = pyrebase.initialize_app(Config)
auth = fb.auth()
db = fb.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'loai'

#Code goes below here

# @app.route('/', methods=['GET', 'POST'])
# def authe():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             login_session['user'] = auth.sign_in_with_email_and_password(email, password)
#             return redirect(url_for('home'))
#         except:
#             print('Auth login Failed')
#     return render_template("auth.html")


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)