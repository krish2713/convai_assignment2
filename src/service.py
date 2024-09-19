
from models import Flight, Hotel, RentalCar, TravelAdvisory  # Import your models

### Function to Query Flights Based on Extracted Entities
def query_flight(departure_city, destination_city, departure_date):
    flights = Flight.query.filter_by(departure=departure_city, destination=destination_city).filter(
        Flight.departure_time >= departure_date).all()
    
    flight_results = []
    for flight in flights:
        flight_text = (
            f"Flight from {flight.departure} to {flight.destination} on {flight.departure_time.strftime('%Y-%m-%d %H:%M')} "
            f"with {flight.airline}. Arrival time: {flight.arrival_time.strftime('%Y-%m-%d %H:%M')}."
        )
        flight_results.append(flight_text)
    
    return flight_results


def query_hotel(location, checkin_date, checkout_date):
    hotels = Hotel.query.filter_by(location=location).filter(
        Hotel.checkin_date <= checkin_date,
        Hotel.checkout_date >= checkout_date).all()

    hotel_results = []
    for hotel in hotels:
        hotel_text = (
            f"Hotel: {hotel.name} located in {hotel.location}.\n"
            f"Available rooms: {hotel.available_rooms}.\n"
            f"Check-in date: {hotel.checkin_date.strftime('%Y-%m-%d')}.\n"
            f"Check-out date: {hotel.checkout_date.strftime('%Y-%m-%d')}.\n"
        )
        hotel_results.append(hotel_text)

    if not hotel_results:
        return ["No hotels found for your request."]
    
    return hotel_results

def query_rental_car(location, pickup_date, dropoff_date):
    cars = RentalCar.query.filter_by(location=location).filter(
        RentalCar.pickup_date <= pickup_date,
        RentalCar.dropoff_date >= dropoff_date).all()

    car_results = []
    for car in cars:
        car_text = (
            f"Rental Car: {car.type} available in {car.location}.\n"
            f"Available count: {car.available_count}.\n"
            f"Pickup date: {car.pickup_date.strftime('%Y-%m-%d')}.\n"
            f"Drop-off date: {car.dropoff_date.strftime('%Y-%m-%d')}.\n"
        )
        car_results.append(car_text)

    if not car_results:
        return ["No rental cars found for your request."]
    
    return car_results

def query_travel_advisory(country):
    advisory = TravelAdvisory.query.filter_by(country=country).first()

    if advisory:
        advisory_text = (
            f"Travel Advisory for {advisory.country}:\n"
            f"{advisory.advisory}\n"
            f"Date of advisory: {advisory.advisory_date.strftime('%Y-%m-%d')}.\n"
        )
        return [advisory_text]
    else:
        return ["No travel advisory found for your request."]


### Main Chatbot Function to Handle Different Intents and Query DB
def retrieve_travelinfo( intent, entities):
    # Define required entities for each intent
    required_entities = {
        "book_flight": ["departure_city", "destination_city", "departure_date"],
        "book_hotel": ["location", "checkin_date", "checkout_date"],
        "rent_car": ["location", "pickup_date", "dropoff_date"],
        "travel_advisory": ["country"]
    }
    # Extract the required entities based on the intent
    missing_entities = []
       # Check for missing entities based on the intent
    if intent == "book_flight":
        departure_city = entities.get("departure_city")
        destination_city = entities.get("destination_city")
        departure_date = entities.get("departure_date")

        if not departure_city:
            missing_entities.append("departure_city")
        if not destination_city:
            missing_entities.append("destination_city")
        if not departure_date:
            missing_entities.append("departure_date")

    elif intent == "book_hotel":
        location = entities.get("location")
        checkin_date = entities.get("checkin_date")
        checkout_date = entities.get("checkout_date")

        if not location:
            missing_entities.append("location")
        if not checkin_date:
            missing_entities.append("checkin_date")
        if not checkout_date:
            missing_entities.append("checkout_date")

    elif intent == "rent_car":
        location = entities.get("location")
        pickup_date = entities.get("pickup_date")
        dropoff_date = entities.get("dropoff_date")

        if not location:
            missing_entities.append("location")
        if not pickup_date:
            missing_entities.append("pickup_date")
        if not dropoff_date:
            missing_entities.append("dropoff_date")

    elif intent == "travel_advisory":
        country = entities.get("country")
        if not country:
            missing_entities.append("country")

    # If there are missing entities, prompt the user to provide the missing information
    if missing_entities:
        response = "I need more information to complete your request. Could you please provide the following: "
        response += ", ".join([entity.replace("_", " ") for entity in missing_entities]) + "?"
        return response

    # If all entities are available, proceed with the database query
    if intent == "book_flight":
        return query_flight(departure_city, destination_city, departure_date)
    elif intent == "book_hotel":
        return query_hotel(location, checkin_date, checkout_date)
    elif intent == "rent_car":
        return query_rental_car(location, pickup_date, dropoff_date)
    elif intent == "travel_advisory":
        return query_travel_advisory(country)
    else:
        return "Sorry, I didn't understand your request."
