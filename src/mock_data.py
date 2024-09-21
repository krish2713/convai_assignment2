from datetime import datetime, timedelta
import random
from db_models import Flight, Hotel, RentalCar, TravelAdvisory,db
# Function to create mock data
def create_mock_data():
    # Airlines, cities, car types, and countries for mock data
    airlines = ['Delta', 'American Airlines', 'Southwest', 'United', 'JetBlue']
    flight_num = ['AB123', 'BC234', 'CD567', 'DE890', 'FG211']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 'San Francisco', 'Boston', 'Seattle']
    car_types = ['SUV', 'Sedan', 'Truck', 'Convertible', 'Minivan']
    countries = ['USA', 'Canada', 'Mexico', 'United Kingdom', 'France', 'Germany', 'Japan', 'Australia']

    advisories = [
        'Travel allowed with caution due to COVID-19 restrictions.',
        'Strict quarantine measures in place for travelers.',
        'No restrictions; normal travel allowed.',
        'Avoid non-essential travel due to ongoing political unrest.',
        'Health advisory: High risk of diseases like malaria.'
    ]
    
    # Insert 10 mock flights
    for i in range(10):
        departure_city = random.choice(cities)
        destination_city = random.choice([city for city in cities if city != departure_city])
        departure_time = datetime.utcnow() + timedelta(days=10 + i)
        arrival_time = departure_time + timedelta(hours=random.randint(2, 6))

        flight = Flight(
            airline=random.choice(airlines),
            flight_no=random.choice(flight_num),
            departure=departure_city,
            destination=destination_city,
            departure_time=departure_time,
            arrival_time=arrival_time
        )
        db.session.add(flight)

    # Insert 10 mock hotels
    for i in range(10):
        checkin_date = datetime.utcnow().date() + timedelta(days=10 + i)
        checkout_date = checkin_date + timedelta(days=random.randint(1, 5))

        hotel = Hotel(
            name=f'Hotel {random.choice(cities)} {i + 1}',
            location=random.choice(cities),
            available_rooms=random.randint(1, 100),
            checkin_date=checkin_date,
            checkout_date=checkout_date
        )
        db.session.add(hotel)

    # Insert 10 mock rental cars
    for i in range(10):
        pickup_date = datetime.utcnow().date() + timedelta(days=10 + i)
        dropoff_date = pickup_date + timedelta(days=random.randint(1, 5))

        car = RentalCar(
            type=random.choice(car_types),
            location=random.choice(cities),
            available_count=random.randint(1, 50),
            pickup_date=pickup_date,
            dropoff_date=dropoff_date
        )
        db.session.add(car)

    # Insert 10 mock travel advisories
    for i in range(10):
        advisory_date = datetime.utcnow().date() + timedelta(days=10 + i)

        advisory = TravelAdvisory(
            country=random.choice(countries),
            advisory=random.choice(advisories),
            advisory_date=advisory_date
        )
        db.session.add(advisory)

    # Commit all the data to the database
    db.session.commit()

