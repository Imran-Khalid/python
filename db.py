from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow
from marshmallow import  fields, post_load

app = Flask(__name__)

some_engine = create_engine('mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='carsales'))

app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='carsales')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)
# create a Session
session = Session()