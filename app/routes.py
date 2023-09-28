from app import app
from flask import render_template, request
from .forms import SignUpForm, LoginForm, SearchForm
from .models import db, User
import requests as r


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    form=SignUpForm()
    if request.method == 'POST':
        print("post request made")
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            #does a user with that username already exist?
            #does a user with that email already exist?

            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()


    return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
                username = form.username.data
                password = form.password.data

            #look in database for user with that username
            #if they exist, see if the passwords match
            #if passwords match, consider them logged in

                user = User(username, password)

                db.session.add(user)
                db.session.commit()

    return render_template('login.html', form=form )


@app.route("/search", methods=["GET", "POST"])
def search_page():
    form= SearchForm()
    if request.method == 'POST':            
            def get_pokemon(name):
                name = form.name.data
                url= f"https://pokeapi.co/api/v2/pokemon/{name}"
                response = r.get(url)
                if response.ok:
                    data= response.json()

                    name = data['species']['name']
                    base_experience = data['base_experience']
                    ability_name = data["abilities"][0]["ability"]["name"]
                    sprite = data["sprites"]["front_shiny"]
                    attack = data["stats"][1]["base_stat"]
                    hp = data["stats"][0]["base_stat"]
                    defense = data["stats"][2]["base_stat"]
                print(name, base_experience, ability_name, hp, attack, sprite, defense)
                
                #return f'(name: {name}, base experience: {base_experience}, ability name: {ability_name}, sprite: {sprite}, attack: {attack}, hp: {hp}, defense: {defense})'
    
       
    
    return render_template("search.html", form=form) 
#pokemon_name=small_dictionary

#small_dictionary = get_pokemon(pokemon_name)


