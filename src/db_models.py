from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Initialize SQLAlchemy without associating it with an app just yet
db = SQLAlchemy()


class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    flight_no = db.Column(db.String(100), nullable=False)
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
    advisory_date = db.Column(db.Date, nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), unique=True, nullable=False) 
    type = db.Column(db.String(50), nullable=False)  # 'flight', 'hotel', 'rental_car'
    traveller_names = db.Column(db.String(200), nullable=False)
    departure_city = db.Column(db.String(100), nullable=True)  # Only for flight/rental_car
    destination_city = db.Column(db.String(100), nullable=True)  # Only for flight
    airline = db.Column(db.String(100), nullable=True) # Only for flight
    flight_no = db.Column(db.String(100), nullable=True) # Only for flight
    location = db.Column(db.String(100), nullable=True)  # Only for hotel
    checkin_date = db.Column(db.String(20), nullable=True)  # Only for hotel
    checkout_date = db.Column(db.String(20), nullable=True)  # Only for hotel
    departure_date = db.Column(db.String(20), nullable=True)  # Only for flight
    return_date = db.Column(db.String(20), nullable=True)  # Only for flight
    pickup_location = db.Column(db.String(100), nullable=True)  # Only for rental car
    dropoff_location = db.Column(db.String(100), nullable=True)  # Only for rental car
    pickup_date = db.Column(db.String(20), nullable=True)  # Only for rental car
    dropoff_date = db.Column(db.String(20), nullable=True)  # Only for rental car
    car_type = db.Column(db.String(50), nullable=True)  # Only for rental car
    status = db.Column(db.String(20), default='booked')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
