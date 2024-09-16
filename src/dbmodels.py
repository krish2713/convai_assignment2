from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

class Hotel(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    available_rooms = db.Column(db.Integer, nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)

class RentalCar(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    available_count = db.Column(db.Integer, nullable=False)
    dropoff_date = db.Column(db.Date, nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)

class TravelAdvisory(db.Model):
    __tablename__ = 'travel_advisories'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    advisory = db.Column(db.Text, nullable=False)