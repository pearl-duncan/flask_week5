from app import app
from flask import flash, redirect, render_template, request, url_for
from .forms import SignUpForm, LoginForm, SearchForm
from .models import db, User, Pokemon
import requests as r
from flask_login import login_user, logout_user, current_user, login_required



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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            # Look in the database for a user with that username
            user = User.query.filter_by(username=username).first() 
            # if they exist, see if the password match
            if user:
                if user.password == password:
            # if passwords match, consider them logged in
                    login_user(user)
                else:
                    print('passwords dont match')
            else:
                print('that user doesnt exist')

        return redirect(url_for('index'))
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route("/search", methods=["GET", "POST"])
def search_page():
    form= SearchForm()
    if request.method == 'POST': 
        if Pokemon == True:
            return render_template("ind_pokemon.html")
        else:
            flash('That pokemon does not exist', 'danger')
            return redirect("search.html")
    return render_template("search.html", form=form)
                 
        
        
        
@app.route("/search/<pokemon_id>")
@login_required
def get_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    url= f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
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
        #return f'(name: {name}, base experience: {base_experience}, ability name: {ability_name}, sprite: {sprite}, attack: {attack}, hp: {hp}, defense: {defense})'
        return render_template("ind_pokemon.html", name=name, base_experience=base_experience, ability_name=ability_name, sprite=sprite, hp=hp, attack=attack, defense=defense )               

          
               
            #print(name, base_experience, ability_name, hp, attack, sprite, defense)
             
                
    
     
#pokemon_name=small_dictionary

#small_dictionary = get_pokemon(pokemon_name)


