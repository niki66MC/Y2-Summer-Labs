from flask import Flask,render_template,redirect,request,url_for,session as login_session
import random
import pyrebase


app = Flask(__name__,template_folder = 'templates',static_folder = "static")


Config = {
  "apiKey": "AIzaSyAFFF8G4IGPjsLBJ8ZQWq5fzJ8donZWhYk",
  "authDomain": "notes-c483d.firebaseapp.com",
  "projectId": "notes-c483d",
  "storageBucket": "notes-c483d.appspot.com",
  "messagingSenderId": "721802140561",
  "appId": "1:721802140561:web:022c6e5bff2c273b415830",
  "databaseURL": "https://notes-c483d-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app.config['SECRET_KEY'] = 'Nadav'





@app.route('/',methods = ["GET","POST"])
def signup():
	if request.method == "POST":
		email = request.form['email']
		password = request.form["password"]
		username = request.form["username"]
		user = {"username": username, "notes" : {"Hello": "Welcome to the note website! You can create and edit notes here!"}}

		error = ""
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email,password)
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('notes'))
		except Exception as e:
			return "Failed to signup"
	else:
		return render_template("signup.html")






@app.route('/signin',methods = ["POST","GET"])
def signin():
	if request.method == "POST":
		error = ""
		email = request.form['email']
		password = request.form["password"]
		try:
			login_session["user"] = auth.sign_in_with_email_and_password(email,password)
			
			return redirect(url_for("notes"))
		except:
			return "Failed to sign in"
	else:
		return render_template("signin.html")


@app.route('/notes', methods = ['POST','GET'])
def notes():
	if request.method == "POST":
		if request.form["is_edit"] == "1":
			note = request.form['text1']
			name1 = request.form['name1']
			past_name = request.form['past_name']
			user1 = db.child("Users").child(login_session['user']['localId']).child("notes").get().val()
			user1.pop(past_name)
			user1[name1] = note
			db.child("Users").child(login_session['user']['localId']).child("notes").set(user1)
			return render_template("notes.html", notes = db.child("Users").child(login_session['user']['localId']).child("notes").get().val())
		else:
			note = request.form['text1']
			name1 = request.form['name1']
			user1 = {name1 : note}
			db.child("Users").child(login_session['user']['localId']).child("notes").update(user1) 
			dict1 = {}
			if type(db.child("Users").child(login_session['user']['localId']).child("notes").get().val()) == type(dict1):
				return render_template("notes.html",notes = db.child("Users").child(login_session['user']['localId']).child("notes").get().val())
			else:
				return render_template("notes.html",notes = {})
	else:
		dict1 = {}
		if type(db.child("Users").child(login_session['user']['localId']).child("notes").get().val()) == type(dict1):
			return render_template("notes.html",notes = db.child("Users").child(login_session['user']['localId']).child("notes").get().val())
		else:
			return render_template("notes.html",notes = {})


@app.route('/editor')
def editor():
	return render_template("editor.html")

@app.route('/edit_note',methods = ["POST"])
def edit_note():

	if request.form["submit"] == "Delete note":
		name1 = request.form['name1']
		user1 = db.child("Users").child(login_session['user']['localId']).child("notes").get().val()
		user1.pop(name1)
		db.child("Users").child(login_session['user']['localId']).child("notes").set(user1)
		dict1 = {}
		if type(db.child("Users").child(login_session['user']['localId']).child("notes").get().val()) == type(dict1):
			return render_template("notes.html",notes = db.child("Users").child(login_session['user']['localId']).child("notes").get().val())
		else:
			return render_template("notes.html",notes = {})
	else:
		return render_template("edit_note.html",name_note = request.form['name1'], notes = db.child("Users").child(login_session['user']['localId']).child("notes").get().val())



@app.route('/old_note/<name_note>')
def old_note(name_note):
	dict1 = {}
	return render_template('old_note.html',note = name_note, notes = db.child("Users").child(login_session['user']['localId']).child("notes").get().val())
@app.route('/signout')
def signout():
	login_session['user'] = None
	auth.current_user = None
	return redirect(url_for('signin'))


if __name__ == '__main__':
	app.run(debug = True)