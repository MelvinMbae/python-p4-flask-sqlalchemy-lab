#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal=Animal.query.filter(Animal.id==id).first()
    
    if not animal:
        return '<404 Animal Not Found>'
    
    return f'''
    <ul>ID:{animal.id}</ul>
    <ul>Name:{animal.name}</ul>
    <ul>Species:{animal.species}</ul>
    <ul>Zookeeper:{animal.zookeeper.name}</ul>
    <ul>Enclosure:{animal.enclosure.environment}</ul>
    '''

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper=Zookeeper.query.filter(Zookeeper.id==id).first()
    if not zookeeper:
        return '<404 Zookeeper Not Found>'
    
    response_body= f'''
        <ul>ID:{zookeeper.id}</ul>
        <ul>Name:{zookeeper.name}</ul>
        <ul>Birthday:{zookeeper.birthday}</ul>
    '''
    for animal in zookeeper.animals:
        response_body += f"<ul>Animal:{animal.name}</ul>"
    
    response = make_response(response_body,200)
    
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    return ''


if __name__ == '__main__':
    app.run(port=5555, debug=True)
