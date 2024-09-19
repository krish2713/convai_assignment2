from datetime import datetime,date
from db_models import Flight, Hotel, RentalCar, TravelAdvisory

flights_data = [
    Flight(airline="Delta Airlines", departure="New York", destination="London", departure_time=datetime(2024, 9, 21, 14, 30), arrival_time=datetime(2024, 9, 21, 22, 45)),
    Flight(airline="American Airlines", departure="Los Angeles", destination="Tokyo", departure_time=datetime(2024, 10, 5, 10, 15), arrival_time=datetime(2024, 10, 6, 14, 30)),
    Flight(airline="Emirates", departure="Dubai", destination="Sydney", departure_time=datetime(2024, 11, 1, 20, 0), arrival_time=datetime(2024, 11, 2, 8, 0)),
    Flight(airline="Qatar Airways", departure="Doha", destination="Paris", departure_time=datetime(2024, 8, 30, 16, 45), arrival_time=datetime(2024, 8, 30, 22, 0)),
    Flight(airline="British Airways", departure="London", destination="New York", departure_time=datetime(2024, 12, 18, 7, 30), arrival_time=datetime(2024, 12, 18, 14, 30)),
    Flight(airline="Air Canada", departure="Toronto", destination="Vancouver", departure_time=datetime(2024, 7, 19, 9, 0), arrival_time=datetime(2024, 7, 19, 11, 45)),
    Flight(airline="Lufthansa", departure="Frankfurt", destination="San Francisco", departure_time=datetime(2024, 9, 25, 11, 0), arrival_time=datetime(2024, 9, 25, 14, 30)),
    Flight(airline="Singapore Airlines", departure="Singapore", destination="New Delhi", departure_time=datetime(2024, 8, 20, 18, 45), arrival_time=datetime(2024, 8, 20, 22, 15)),
    Flight(airline="Cathay Pacific", departure="Hong Kong", destination="Melbourne", departure_time=datetime(2024, 11, 10, 23, 55), arrival_time=datetime(2024, 11, 11, 10, 30)),
    Flight(airline="KLM", departure="Amsterdam", destination="Rio de Janeiro", departure_time=datetime(2024, 9, 30, 13, 0), arrival_time=datetime(2024, 9, 30, 22, 0))
   ]
hotels_data = [
    Hotel(name="The Plaza", location="New York", available_rooms=10, checkin_date=date(2024, 9, 21), checkout_date=date(2024, 9, 25)),
    Hotel(name="Hilton Tokyo", location="Tokyo", available_rooms=5, checkin_date=date(2024, 10, 5), checkout_date=date(2024, 10, 10)),
    Hotel(name="Burj Al Arab", location="Dubai", available_rooms=2, checkin_date=date(2024, 11, 1), checkout_date=date(2024, 11, 4)),
    Hotel(name="Ritz Paris", location="Paris", available_rooms=8, checkin_date=date(2024, 8, 30), checkout_date=date(2024, 9, 2)),
    Hotel(name="The Ritz-Carlton", location="London", available_rooms=15, checkin_date=date(2024, 12, 18), checkout_date=date(2024, 12, 22)),
    Hotel(name="Fairmont Royal York", location="Toronto", available_rooms=20, checkin_date=date(2024, 7, 19), checkout_date=date(2024, 7, 22)),
    Hotel(name="Grand Hyatt", location="San Francisco", available_rooms=9, checkin_date=date(2024, 9, 25), checkout_date=date(2024, 9, 28)),
    Hotel(name="Marina Bay Sands", location="Singapore", available_rooms=6, checkin_date=date(2024, 8, 20), checkout_date=date(2024, 8, 23)),
    Hotel(name="Crown Towers", location="Melbourne", available_rooms=12, checkin_date=date(2024, 11, 10), checkout_date=date(2024, 11, 13)),
    Hotel(name="Copacabana Palace", location="Rio de Janeiro", available_rooms=7, checkin_date=date(2024, 9, 30), checkout_date=date(2024, 10, 5))
]

rental_cars_data = [
    RentalCar(type="SUV", location="New York", available_count=4, pickup_date=date(2024, 9, 21), dropoff_date=date(2024, 9, 25)),
    RentalCar(type="Sedan", location="Tokyo", available_count=3, pickup_date=date(2024, 10, 5), dropoff_date=date(2024, 10, 10)),
    RentalCar(type="Luxury", location="Dubai", available_count=1, pickup_date=date(2024, 11, 1), dropoff_date=date(2024, 11, 4)),
    RentalCar(type="Compact", location="Paris", available_count=6, pickup_date=date(2024, 8, 30), dropoff_date=date(2024, 9, 2)),
    RentalCar(type="SUV", location="London", available_count=5, pickup_date=date(2024, 12, 18), dropoff_date=date(2024, 12, 22)),
    RentalCar(type="Sedan", location="Toronto", available_count=7, pickup_date=date(2024, 7, 19), dropoff_date=date(2024, 7, 22)),
    RentalCar(type="Luxury", location="San Francisco", available_count=2, pickup_date=date(2024, 9, 25), dropoff_date=date(2024, 9, 28)),
    RentalCar(type="SUV", location="Singapore", available_count=3, pickup_date=date(2024, 8, 20), dropoff_date=date(2024, 8, 23)),
    RentalCar(type="Compact", location="Melbourne", available_count=8, pickup_date=date(2024, 11, 10), dropoff_date=date(2024, 11, 13)),
    RentalCar(type="Luxury", location="Rio de Janeiro", available_count=2, pickup_date=date(2024, 9, 30), dropoff_date=date(2024, 10, 5))
]

travel_advisories_data = [
    TravelAdvisory(country="United States", advisory="Travel restrictions in some states due to weather conditions.", advisory_date=date(2024, 9, 15)),
    TravelAdvisory(country="Japan", advisory="Typhoon season: Expect flight delays and potential cancellations.", advisory_date=date(2024, 10, 2)),
    TravelAdvisory(country="United Arab Emirates", advisory="High temperatures: Stay hydrated and avoid outdoor activities during midday.", advisory_date=date(2024, 11, 1)),
    TravelAdvisory(country="France", advisory="Protests expected in major cities: Avoid crowded areas and monitor local news.", advisory_date=date(2024, 8, 28)),
    TravelAdvisory(country="United Kingdom", advisory="Rail strikes may impact travel plans. Check schedules in advance.", advisory_date=date(2024, 12, 17)),
    TravelAdvisory(country="Canada", advisory="Forest fires in western regions: Air quality warnings in effect.", advisory_date=date(2024, 7, 17)),
    TravelAdvisory(country="Singapore", advisory="Heavy rain expected: Plan for potential delays in transportation.", advisory_date=date(2024, 8, 19)),
    TravelAdvisory(country="Australia", advisory="Bushfire season: Stay updated on fire alerts and evacuation routes.", advisory_date=date(2024, 11, 9)),
    TravelAdvisory(country="Brazil", advisory="Increased crime in some areas of Rio de Janeiro: Exercise caution.", advisory_date=date(2024, 9, 28)),
    TravelAdvisory(country="Italy", advisory="Heatwave expected across the country: Stay indoors during peak hours.", advisory_date=date(2024, 9, 14))
]

