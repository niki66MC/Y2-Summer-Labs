from flask import Flask,render_template,redirect,request,url_for,session as login_session
import random
import pyrebase


app = Flask(__name__,template_folder = 'templates',static_folder = "static")

app.config['SECRET_KEY'] = 'Nadav'



Config = {
  "apiKey": "AIzaSyAwoFcWa5OwyFh-8TIL9_PhomXQqnCwGLE",
  "authDomain": "eitan-40d22.firebaseapp.com",
  "databaseURL": "https://eitan-40d22-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "eitan-40d22",
  "storageBucket": "eitan-40d22.appspot.com",
  "messagingSenderId": "1016569198091",
  "appId": "1:1016569198091:web:e29a5fe109ae8eebbc790e",
  "databaseURL" : "https://eitan-40d22-default-rtdb.europe-west1.firebasedatabase.app/"

}


firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()


@app.route('/',methods = ["GET","POST"])
def signup():
	if request.method == "POST":
		login_session["email"] = request.form['email']
		login_session["password"] = request.form["password"]
		login_session["quotes"] = []
		login_session.modified = True

		error = ""
		try:
			login_session['user'] = auth.create_user_with_email_and_password(login_session["email"],login_session["password"])
			user = {"full_name": request.form["full_name"], "username": request.form["username"],"email": request.form["email"]}
			db.child("Users").child(login_session['user']["localId"]).set(user)

			return redirect(url_for('home'))
		except:
			error = "Auth failed"
	else:
		return render_template("signup.html")

@app.route('/signin',methods = ["POST","GET"])
def signin():
	if request.method == "POST":
		error = ""
		login_session["email"] = request.form['email']
		login_session["password"] = request.form["password"]
		login_session["quotes"] = []
		login_session.modified = True
		try:
			login_session["user"] = auth.sign_in_with_email_and_password(login_session["email"],login_session["password"])
			
			return redirect(url_for("home"))
		except:
			error = 'Auth failed'
	else:
		return render_template("signin.html")


@app.route('/home', methods = ["GET","POST"])
def home():
	if request.method == "POST":
		login_session["quotes"].append(request.form["quote"])
		login_session.modified = True
		return redirect(url_for("thanks"))
	else:
		return render_template("home.html")


@app.route('/display')
def display():
	login_session.modified = True
	return render_template("display1.html", quotes = login_session['quotes'])


@app.route('/thanks')
def thanks():
	return render_template("thanks.html")



@app.route('/signout')
def signout():
	login_session['user'] = None
	auth.current_user = None
	return redirect(url_for('signin'))



if __name__ == '__main__':
	app.run(debug = True)