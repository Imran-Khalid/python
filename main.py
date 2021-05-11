from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
some_engine = create_engine('mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='carsales'))

app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='carsales')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

@app.route('/', methods =['GET','POST'])
def home():
    cars = Car.query.all()
    return render_template('index.html', cars = cars) 

@app.route('/add', methods =['GET','POST'])
def add():
    if request.method=='POST':
        name = request.form['name']
        model = request.form['model']
        number = request.form['number']
        desc = request.form['desc']
        car = Car(name=name, model=model, number=number, desc=desc)
        db.session.add(car)
        db.session.commit()
        cars = Car.query.all()
        return render_template('index.html', cars = cars) 
    return render_template('add.html') 

@app.route('/update/<int:id>', methods =['GET','POST'])
def update(id):
    if request.method=='POST':
        name = request.form['name']
        model = request.form['model']
        number = request.form['number']
        desc = request.form['desc']
        car = Car.query.filter_by(id=id).first()
        car.name=name
        car.model=model
        car.number=number
        car.desc=desc
        db.session.add(car)
        db.session.commit()
        return redirect("/")

    cars = Car.query.filter_by(id=id).first()
    return render_template('update.html', car = cars) 

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
        return render_template('search.html', cars = cars) 
     
if __name__ == '__main__':
   app.run(debug = True)