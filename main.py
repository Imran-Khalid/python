from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow
from marshmallow import  fields, post_load

app = Flask(__name__)
some_engine = create_engine('mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='carsales'))

app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='carsales')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)
# create a Session
session = Session()

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

@app.route('/', methods =['GET','POST'])
def home():
    cars = Car.query.all()
    results = cars_schema.dump(cars)
    return render_template('index.html', cars = results) 

@app.route('/add', methods =['GET','POST'])
def add():
    if request.method=='POST':
        input_data = {}
        input_data['name'] = request.form['name']
        input_data['model'] = request.form['model']
        input_data['number'] = request.form['number']
        input_data['desc'] = request.form['desc']
        result = car_schema.load(input_data)
        db.session.add(result)
        db.session.commit()
        return redirect("/")

    return render_template('add.html') 

@app.route('/update/<int:id>', methods =['GET','POST'])
def update(id):
    if request.method=='POST':
        name = request.form['name']
        model = request.form['model']
        number = request.form['number']
        desc = request.form['desc']
        input_data = {}
        input_data['name'] = name
        input_data['model'] = model
        input_data['number'] = number
        input_data['desc'] = desc
        result = car_schema.load(input_data)
        if(result):
            car = Car.query.filter_by(id=id).first()
            car.name=name
            car.model=model
            car.number=number
            car.desc=desc
            db.session.commit()
            return redirect("/")
        return redirect("/")

    my_car = Car.query.filter_by(id=id).first()
    result = car_schema.dump(my_car)
    return render_template('update.html', car = result) 

@app.route('/delete/<int:id>')
def delete(id):
    car = Car.query.filter_by(id=id).first()
    db.session.delete(car)
    db.session.commit()
    return redirect("/")

@app.route('/search', methods =['GET','POST'])
def search():
    if request.method=='POST':
        text = request.form['search']
        search = "%{}%".format(text)
        cars = Car.query.filter(Car.name.like(search)).all()
        results = cars_schema.dump(cars)
        return render_template('search.html', cars = results) 
     
if __name__ == '__main__':
   app.run(debug = True)