from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from model import Car, car_schema,cars_schema
from db import db, app , session
from sqlalchemy import create_engine


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