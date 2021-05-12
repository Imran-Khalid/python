from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow
from marshmallow import  fields, post_load
from db import ma,session,db
class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    model = db.Column(db.String(200))
    number = db.Column(db.String(200))
    desc = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self , name, model, number, desc):
        self.name = name
        self.model = model
        self.number = number
        self.desc = desc

class CarSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    model = fields.Integer()
    number = fields.Integer()
    desc = fields.String()

    @post_load
    def create_car(self, data, **kwargs):
        return Car(**data)

    class Meta:
        fields = ("id", "name", "model", "number", "desc")

car_schema = CarSchema()
cars_schema = CarSchema(many=True)
