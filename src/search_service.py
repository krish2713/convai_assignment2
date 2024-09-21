
from db_models import Flight, Hotel, RentalCar, TravelAdvisory,Booking,db  # Import your models
from sqlalchemy import distinct
import json

### Function to Query Flights Based on Extracted Entities
def query_flight(departure_city, destination_city, departure_date):
    flights = Flight.query.filter_by(departure=departure_city, destination=destination_city).filter(
        Flight.departure_time >= departure_date).all()
    flight_results = []
    for flight in flights:
        flight_text = (
            f"Found Flight {flight.flight_no} from {flight.departure} to {flight.destination} on {flight.departure_time.strftime('%Y-%m-%d %H:%M')} "
            f"with {flight.airline} Arrival time {flight.arrival_time.strftime('%Y-%m-%d %H:%M')}."
        )
        flight_results.append(flight_text)
    if not flight_results:
        return "No Flights found for your request"
    else:
        return  ", ".join(flight_results)

def query_hotel(location, checkin_date, checkout_date):
    hotels = Hotel.query.filter_by(location=location).filter(
        Hotel.checkin_date <= checkin_date,
        Hotel.checkout_date >= checkout_date).all()

    hotel_results = []
    for hotel in hotels:
        hotel_text = (
            f"Found Hotel: {hotel.name} located in {hotel.location} "
            f"Available rooms: {hotel.available_rooms} "
            f"Check-in date: {hotel.checkin_date.strftime('%Y-%m-%d')} "
            f"Check-out date: {hotel.checkout_date.strftime('%Y-%m-%d')} "
        )
        hotel_results.append(hotel_text)

    if not hotel_results:
        return "No hotels found for your request"
    else:
        return ", ".join(hotel_results)
 
def query_rental_car(location, pickup_date, dropoff_date):
    cars = RentalCar.query.filter_by(location=location).filter(
        RentalCar.pickup_date <= pickup_date,
        RentalCar.dropoff_date >= dropoff_date).all()

    car_results = []
    for car in cars:
        car_text = (
            f"Rental Car: {car.type} available in {car.location}"
            f"Available count: {car.available_count}"
            f"Pickup date: {car.pickup_date.strftime('%Y-%m-%d')}"
            f"Drop-off date: {car.dropoff_date.strftime('%Y-%m-%d')}"
        )
        car_results.append(car_text)

    if not car_results:
        return "No rental found for your request"
    else:
        return ", ".join(car_results)

def query_travel_advisory(country):
    advisory = TravelAdvisory.query.filter_by(country=country).first()

    if advisory:
        advisory_text = (
            f"Travel Advisory for {advisory.country}:"
            f"{advisory.advisory}"
            f"Date of advisory: {advisory.advisory_date.strftime('%Y-%m-%d')}"
        )
        return [advisory_text]
    else:
        return ["No travel advisory found for your request"]


### Main Chatbot Function to Handle Different Intents and Query DB
def retrieve_travelinfo( intent, entities, user_id):
    # Define required entities for each intent
    required_entities = {
        "SearchFlight": ["departure_city", "destination_city", "departure_date"],
        "SearchHotel": ["location", "checkin_date", "checkout_date"],
        "SearchRentCar": ["location", "pickup_date", "dropoff_date"],
        "TravelAdvisory": ["country"]
         }
    # Extract the required entities based on the intent
    missing_entities = []
       # Check for missing entities based on the intent
    if intent == "SearchFlight":
        departure_city = entities.get("departure_city")
        destination_city = entities.get("destination_city")
        departure_date = entities.get("departure_date")

        if not departure_city:
            missing_entities.append("departure_city")
        if not destination_city:
            missing_entities.append("destination_city")
        if not departure_date:
            missing_entities.append("departure_date")

    elif intent == "SearchHotel":
        location = entities.get("location")
        checkin_date = entities.get("checkin_date")
        checkout_date = entities.get("checkout_date")

        if not location:
            missing_entities.append("location")
        if not checkin_date:
            missing_entities.append("checkin_date")
        if not checkout_date:
            missing_entities.append("checkout_date")

    elif intent == "SearchRentCar":
        location = entities.get("location")
        pickup_date = entities.get("pickup_date")
        dropoff_date = entities.get("dropoff_date")

        if not location:
            missing_entities.append("location")
        if not pickup_date:
            missing_entities.append("pickup_date")
        if not dropoff_date:
            missing_entities.append("dropoff_date")

    elif intent == "TravelAdvisory":
        country = entities.get("country")
        if not country:
            missing_entities.append("country")

    # If there are missing entities, prompt the user to provide the missing information
    if missing_entities:
        response = "Missing the following: "
        response += ", ".join([entity.replace("_", " ") for entity in missing_entities]) + "?"
        return response
    
    # If all entities are available, proceed with the database query
    if intent == "SearchFlight":
        return query_flight(departure_city, destination_city, departure_date)
    elif intent == "SearchHotel":
        return query_hotel(location, checkin_date, checkout_date)
    elif intent == "SearchRentCar":
        return query_rental_car(location, pickup_date, dropoff_date)
    elif intent == "TravelAdvisory":
        return query_travel_advisory(country)
    elif intent == "TravelRecommendations":
        return query_user_preferences()
    else:
        return "Sorry, I didn't understand your request."

def query_user_preferences():
    distinct_values = (
        db.session.query(
            Booking.destination_city, 
            Booking.location, 
            Booking.car_type
        )
        .filter(
            (Booking.destination_city != None) | 
            (Booking.location != None) | 
            (Booking.car_type != None)
        )
        .distinct()
        .all()
    )
    # Optionally, you can process the result into a list of dictionaries
    result = [
        {
            'destination_city': dest_city,
            'location': loc,
            'car_type': car
        } 
        for dest_city, loc, car in distinct_values
    ]
    return f"Travel recommendations based on these preferences {json.dumps(result)}"