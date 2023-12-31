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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            #does a user with that username already exist?
            #does a user with that email already exist?

            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()

            flash('Successfully created your account. Log in now.', "success")
            return redirect(url_for('login_page'))
        else:
            flash('Invalid form. Please try again.', 'error')
            
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
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect username/password combination.', 'danger')
            else:
                flash('That username does not exist.', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route("/search", methods=["GET", "POST"])
def search_page():
    form= SearchForm()
    if request.method == 'POST': 
        if form.validate():
            name = form.name.data
            found = Pokemon.query.filter_by(name=name).first()
            if found:
                print("from database")
                return render_template("ind_pokemon.html", pokemon=found)
            else:
                print("from api")
                url= f"https://pokeapi.co/api/v2/pokemon/{name}"
                response = r.get(url)
                if response.ok:
                    data= response.json()
                    p = {
                        'name': data['name'],
                        'base_experience': data['base_experience'],
                        'ability_name': data["abilities"][0]["ability"]["name"],
                        'sprite': data["sprites"]["front_shiny"],
                        'attack': data["stats"][1]["base_stat"],
                        'hp' : data["stats"][0]["base_stat"],
                        'defense' : data["stats"][2]["base_stat"],
                        }
                    pokemon= Pokemon(name=p['name'], base_experience=p["base_experience"], ability_name=p["ability_name"], sprite=p["sprite"], attack=p["attack"], hp=p['hp'], defense=p["defense"])
                    db.session.add(pokemon)
                    db.session.commit()
                    return render_template('ind_pokemon.html', pokemon=pokemon)
            
    return render_template("search.html", form=form)
                 
        
        
        
@app.route("/search/<Pokemon_name>")
def get_pokemon(Pokemon_name):
    pokemon = Pokemon.query.get(Pokemon_name)
    url= f"https://pokeapi.co/api/v2/pokemon/{Pokemon_name}"
    response = r.get(url)
    if response.ok:
        data= response.json()
        my_pokemon = {
            'name': data['species']['name'],
            'base_experience': data['base_experience'],
            'ability_name': data["abilities"][0]["ability"]["name"],
            'sprite': data["sprites"]["front_shiny"],
            'attack': data["stats"][1]["base_stat"],
            'hp' : data["stats"][0]["base_stat"],
            'defense' : data["stats"][2]["base_stat"],
            }
        #return f'(name: {name}, base experience: {base_experience}, ability name: {ability_name}, sprite: {sprite}, attack: {attack}, hp: {hp}, defense: {defense})'
        return render_template("ind_pokemon.html", my_pokemon=my_pokemon)  
          
@app.route("/catch/<pokemon_id>")
@login_required
def caught_pokemon(pokemon_id):
    pokemon = Pokemon.query.filter_by(name=pokemon_id).first()
    if pokemon and len(current_user.pokemon) < 5:
        flash('caught pokemon')
        current_user.pokemon.append(pokemon)
        db.session.commit()
    return redirect(url_for('team', pokemon_id=pokemon_id))

@app.route('/delete/<pokemon_id>')
@login_required
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.filter_by(name=pokemon_id).first()
    if not pokemon:
        flash('That pokemon does not exist', 'danger')
        return redirect(url_for('team'))
    if current_user.id != pokemon.user_id:
        flash('You cannot delete another user\'s catches', 'danger')
        return redirect(url_for('ind_pokemon', post_id=pokemon_id))
    
    db.session.delete(pokemon)
    db.session.commit()
    flash('Successfully deleted your pokemon', 'success')
    return redirect(url_for('team'))

@app.route('/team')
@login_required
def team():
    pokemon = current_user.pokemon
    return render_template('team.html', pokemon=pokemon)

@app.route('/people')
@login_required
def people_page():
    users = User.query.order_by(User.username).filter(User.username != current_user.username).all()
    caught_pokemon = Pokemon.query.order_by(Pokemon.name).all()

    return render_template('people.html', users=users, pokemon=caught_pokemon)


@app.route('/battle/<user_id>')
@login_required
def battle_page(user_id):
    opponent = User.query.filter_by(id=user_id).first()
    opponent_hp=0
    opponent_attack=0
    opponent_defense=0
    for pokemon in opponent.pokemon:
        opponent_hp += int(pokemon.hp)
        opponent_attack += int(pokemon.attack)
        opponent_defense += int(pokemon.defense)
   
    current_user_hp=0
    current_user_attack=0
    current_user_defense=0
    for pokemon in current_user.pokemon:
        current_user_hp += int(pokemon.hp)
        current_user_attack += int(pokemon.attack)
        current_user_defense += int(pokemon.defense)

    current_user_finish=current_user_hp + current_user_defense - opponent_attack
    opponent_finish = opponent_hp + opponent_defense - current_user_attack

    return "i win" if current_user_finish > opponent_finish else "opponent wins"
     