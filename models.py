import sqlite3

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy_utils import database_exists, create_database
from flask import current_app

db = SQLAlchemy()
ma = Marshmallow()

def create_db(app):
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    
    db.init_app(app)
    ma.init_app(app)

    db.create_all()

    return db

class User(db.Model):
    
    __tablename__ = 'users'

    # Storing only the necessary columns
    id = db.Column(db.String(10), primary_key=True)
    deleted = db.Column(db.Boolean(), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable =False)
    is_app_user = db.Column(db.Boolean(), nullable =False)
    is_bot = db.Column(db.Boolean(), nullable =False)
    is_owner = db.Column(db.Boolean(), nullable =False)
    is_primary_owner = db.Column(db.Boolean(), nullable =False)
    is_restricted = db.Column(db.Boolean(), nullable =False)
    is_ultra_restricted = db.Column(db.Boolean(), nullable =False)
    real_name = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    team_id = db.Column(db.String(50), nullable=False)
