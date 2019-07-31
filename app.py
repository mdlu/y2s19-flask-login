from databases import *
from flask import Flask, request, redirect, render_template
from flask import session as login_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def home():
    return render_template('home.html')
    

@app.route('/login', methods=['POST'])
def login():
    user = get_user(request.form['username'])
    if user != None and user.verify_password(request.form["password"]):
        login_session['name'] = user.username
        login_session['logged_in'] = True
        return logged_in()
    else:
        return home()


@app.route('/signup', methods=['POST'])
def signup():
    #check that username isn't already taken
    user = get_user(request.form['username'])
    if user == None:
        add_user(request.form['username'],request.form['password'])
    return home()


@app.route('/logged-in', methods=["GET","POST"])
def logged_in():
    return render_template('logged.html')


@app.route('/logout')
def logout():
    login_session['logged_in'] = False
    return home()
    

@app.route('/update_food', methods = ["GET","POST"])
def food_change():
    if request.method == "POST":
        favorite_food = request.form['fav_food']
        username = login_session['name']
        login_session['fav_food'] = favorite_food
        change_fav_food(username, favorite_food)
        return logged_in()

if __name__ == '__main__':
    app.run(debug=True)