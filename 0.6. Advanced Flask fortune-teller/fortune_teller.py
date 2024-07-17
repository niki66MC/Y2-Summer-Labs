from flask import Flask,render_template,redirect
import random as rand

app = Flask(__name__,template_folder = 'templates')

@app.route('/')
def defuelt():
	return redirect('/home',302) 

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/fortune')
def fortune():
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

	return render_template('fortune.html',fortune = fortunes[rand.randint(0,9)])



if __name__ == '__main__':
	app.run(debug = True)