from flask import Flask,render_template,redirect,request,url_for
from flask import session as login_session
import random

app = Flask(__name__,template_folder = 'templates')

app.config['SECRET_KEY'] = "Nadav"

fortunes = [
"A fresh start will put you on your way.",
"Adventure awaits you this week.",
"Your hard work will soon pay off.",
"A friend will bring you unexpected joy.",
"Success is in your future, stay positive!",
"You will meet someone special soon.",
"An opportunity will arise, seize it!",
"Your creativity will shine in the coming days.",
"Patience is key; good things come to those who wait.",
"A financial gain is on the horizon."
]



@app.route('/', methods = ["GET","POST"])
def defuelt():
    if request.method == "GET":
        return render_template("defu.html")
    else:
        login_session['username'] = request.form['username']
        login_session['birth_month'] = request.form['birth_month']
        return redirect(url_for("home"))

	

@app.route('/home')
def home():
    return render_template('home.html',username = login_session["username"])

@app.route('/fortune')
def fortune():
	return render_template('fortune.html',fortune = fortunes[len(login_session["birth_month"])%10])

@app.route('/indecisive')
def indecisive():
    indecisive_fortunes = []
    fortunes_updated = fortunes.copy()
    for i in range(3):
        n = random.randint(0,len(fortunes_updated)-1)
        indecisive_fortunes.append(fortunes_updated[n])
        fortunes_updated.remove(fortunes_updated[n])
    return render_template('indecisive.html', indecisive_fortunes = indecisive_fortunes)
if __name__ == '__main__':
	app.run(debug = True)