from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45)) 

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_experience = db.Column(db.String(100), nullable=False)
    ability_name = db.Column(db.String(50), nullable=False)
    sprite = db.Column(db.String, nullable=False)
    attack = db.Column(db.String(100), nullable=False)
    hp = db.Column(db.String(100), nullable=False)
    defense = db.Column(db.String(100), nullable=False)

    def __init__(self, name, base_experience, ability_name, sprite, attack, hp, defense):
        self.name = name
        self.ability_name = ability_name
        self.base_experience= base_experience
        self.sprite = sprite
        self.attack = attack
        self.hp = hp
        self.defense = defense

caught = db.Table('caught',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), nullable=False, primary_key=True),
    )