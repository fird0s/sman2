from flask import Flask, url_for, redirect, render_template 
from urls import *
sman2 = Flask(__name__)

@sman2.route('/')
def index():
	return render_template("index.html")


@sman2.route('/profile/')
def profile():
	return render_template("profile.html")

@sman2.errorhandler(404)
def not_found(error):
	return redirect(url_for('index'))

if __name__ == "__main__":
	sman2.debung = True
	sman2.run()

