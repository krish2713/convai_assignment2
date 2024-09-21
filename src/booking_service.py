
from datetime import datetime
from db_models import Booking, db


# Helper function to get current time
def current_time():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def create_booking(intent, entities, user_id):
    # Define required entities for each intent
    required_entities = {
        "BookFlight": ["departure_city", "destination_city", "departure_date"],
        "BookHotel": ["location", "checkin_date", "checkout_date"],
        "RentCar": ["location", "pickup_date", "dropoff_date"],
        "CancelFlight": ["booking_id"],
        "GetFlight": ["booking_id"]
         }
    # Extract the required entities based on the intent
    missing_entities = []
       # Check for missing entities based on the intent
    if intent == "BookFlight":
        print('inside BookFlight')
        departure_city = entities.get("departure_city")
        destination_city = entities.get("destination_city")
        departure_date = entities.get("departure_date")
        traveller_names = entities.get("traveller_names")

        if not departure_city:
            missing_entities.append("departure_city")
        if not destination_city:
            missing_entities.append("destination_city")
        if not departure_date:
            missing_entities.append("departure_date")
        if not traveller_names:
            missing_entities.append("traveller_names")

    elif intent == "BookHotel":
        location = entities.get("location")
        checkin_date = entities.get("checkin_date")
        checkout_date = entities.get("checkout_date")
        traveller_names = entities.get("traveller_names")

        if not location:
            missing_entities.append("location")
        if not checkin_date:
            missing_entities.append("checkin_date")
        if not checkout_date:
            missing_entities.append("checkout_date")
        if not traveller_names:
            missing_entities.append("traveller_names")

    elif intent == "RentCar":
        location = entities.get("location")
        pickup_date = entities.get("pickup_date")
        dropoff_date = entities.get("dropoff_date")
        traveller_names = entities.get("traveller_names")

        if not location:
            missing_entities.append("location")
        if not pickup_date:
            missing_entities.append("pickup_date")
        if not dropoff_date:
            missing_entities.append("dropoff_date")
        if not traveller_names:
            missing_entities.append("traveller_names")

    elif intent.startswith('Cancel') or intent.startswith('Get'):
        booking_id = entities.get("booking_id")
        if not booking_id:
            missing_entities.append("booking_id")

    # If there are missing entities, prompt the user to provide the missing information
    if missing_entities:
        response = "Missing the following: "
        response += ", ".join([entity.replace("_", " ") for entity in missing_entities]) + "?"
        return response

    # If all entities are available, proceed with the database query
    if intent == "BookFlight":
        return create_new_booking(entities, "flight",user_id)
    elif intent == "BookHotel":
       return create_new_booking(entities, "hotel",user_id)
    elif intent == "RentCar":
        return create_new_booking(entities, "car",user_id)
    elif intent.startswith('Get'):
        return get_booking(entities.get("booking_id"))
    elif intent.startswith('Cancel'):
        return cancel_booking(entities.get("booking_id"))
    else:
        return "Sorry, I didn't understand your request."
    

# Endpoint for Booking Management
def create_new_booking(booking_data,booking_type, userId):
    booking = None
   # Flight Booking
    if booking_type == 'flight':
        booking = Booking(
            type='flight',
            traveller_names=", ".join(booking_data.get('traveller_names', [])),
            departure_city=booking_data.get('departure_city'),
            destination_city=booking_data.get('destination_city'),
            departure_date=booking_data.get('departure_date'),
            return_date=booking_data.get('return_date'),
            status='booked',
            created_at=datetime.utcnow(),
            user_id=userId
        )

    # Hotel Booking
    elif booking_type == 'hotel':
        booking = Booking(
            type='hotel',
            traveller_names=", ".join(booking_data.get('traveller_names', [])),
            location=booking_data.get('location'),
            checkin_date=booking_data.get('checkin_date'),
            checkout_date=booking_data.get('checkout_date'),
            status='booked',
            created_at=datetime.utcnow(),
            user_id=userId
        )
    
    # Rental Car Booking
    elif booking_type == 'car':
        booking = Booking(
            type='rental_car',
            traveller_names=", ".join(booking_data.get('traveller_names', [])),
            pickup_location=booking_data.get('pickup_location'),
            dropoff_location=booking_data.get('dropoff_location'),
            pickup_date=booking_data.get('pickup_date'),
            dropoff_date=booking_data.get('dropoff_date'),
            car_type=booking_data.get('car_type'),
            status='booked',
            created_at=datetime.utcnow(),
            user_id=userId
        )
        
    if(booking):
        print(f"booking: {booking}")
        # Save booking to the database
        db.session.add(booking)
        db.session.commit()
        return f'{booking_type.capitalize()} booking created successfully! Booking ID: {booking.id} Travellers: {booking.traveller_names} Status: {booking.status} Created At: {booking.created_at}'

def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        # Create a list to store non-null fields
        booking_details = [f'Booking ID: {booking.id}']
        # Append only non-null fields
        if booking.type is not None:
            booking_details.append(f'Type: {booking.type}')
        if booking.traveller_names is not None:
            booking_details.append(f'Travellers: {booking.traveller_names}')
        if booking.status is not None:
            booking_details.append(f'Status: {booking.status}')
        if booking.created_at is not None:
            booking_details.append(f'Created At: {booking.created_at}')
        if booking.departure_city is not None:
            booking_details.append(f'Departure City: {booking.departure_city}')
        if booking.destination_city is not None:
            booking_details.append(f'Destination City: {booking.destination_city}')
        if booking.location is not None:
            booking_details.append(f'Location: {booking.location}')
        if booking.checkin_date is not None:
            booking_details.append(f'Check-in Date: {booking.checkin_date}')
        if booking.checkout_date is not None:
            booking_details.append(f'Checkout Date: {booking.checkout_date}')
        if booking.departure_date is not None:
            booking_details.append(f'Departure Date: {booking.departure_date}')
        if booking.return_date is not None:
            booking_details.append(f'Return Date: {booking.return_date}')
        if booking.pickup_location is not None:
            booking_details.append(f'Pickup Location: {booking.pickup_location}')
        if booking.dropoff_location is not None:
            booking_details.append(f'Dropoff Location: {booking.dropoff_location}')
        if booking.pickup_date is not None:
            booking_details.append(f'Pickup Date: {booking.pickup_date}')
        if booking.dropoff_date is not None:
            booking_details.append(f'Dropoff Date: {booking.dropoff_date}')
        if booking.car_type is not None:
            booking_details.append(f'Car Type: {booking.car_type}')

        # Return the concatenated string of non-null fields
        return ' '.join(booking_details)

    return "Booking not found."

def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        if booking.status == 'cancelled':
            return f'Error: Booking {booking_id} is already cancelled.'

        booking.status = 'cancelled'
        db.session.commit()
        return f'Booking {booking_id} cancelled successfully! Travellers: {booking.traveller_names} Status: {booking.status} Cancelled At: {current_time()}'
    else:
        return f'Error: Booking with ID {booking_id} not found.'


