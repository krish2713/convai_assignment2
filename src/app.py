from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import spacy


from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments

from db_models import db, Flight # Import the db instance from models
from mock_data import flights_data,hotels_data,rental_cars_data,travel_advisories_data
from service import retrieve_travelinfo

def create_app():
    # Load a pre-trained GPT-2 model and tokenizer
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    # Load a pretrained spaCy NLP model (or transformers model for advanced use)
    nlp = spacy.load("en_core_web_sm")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_info.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
 
    def init_db():
        db.create_all()
        db.session.add_all(flights_data)
        db.session.add_all(hotels_data)
        db.session.add_all(rental_cars_data)
        db.session.add_all(travel_advisories_data)
        db.session.commit()

    # Initialize the app with SQLAlchemy
    with app.app_context():
        # Check if the SQLite database file exists (for SQLite only)
        if not os.path.exists(app.instance_path+'/travel_info.db'):
            print("Database does not exist, creating...")
            # Create all tables
            init_db()
            print("Database and tables created.")
        else:
            print("Database already exists.")

    # Generate a response using GPT-2
    def generate_response(user_input, context_data):
        # Prepare and tokenize the prompt
        prompt = prepare_prompt(user_input, context_data)
        inputs = tokenize_prompt(prompt)

        # Generate output from GPT-2
        output = model.generate(**inputs, max_length=1024, do_sample=True, temperature=0.7)
        
        # Decode the output tokens back into text
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        return response
    
    def extract_travel_entities(user_input):
        doc = nlp(user_input)
        entities = {
            "departure_city": None,
            "destination_city": None,
            "checkin_date": None,
            "checkout_date": None,
            "departure_date": None,
            "return_date": None,
            "pickup_date": None,
            "dropoff_date": None,
            "organization": None,
            "country": None,  # For travel advisory
            "price": None
        }
        
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                if not entities["departure_city"]:
                    entities["departure_city"] = ent.text  # Assume first GPE is the departure city
                else:
                    entities["destination_city"] = ent.text  # Assume second GPE is the destination
            elif ent.label_ == 'DATE':
                # Assign dates based on context
                if "check-in" in user_input or "hotel" in user_input:
                    if not entities["checkin_date"]:
                        entities["checkin_date"] = ent.text
                    else:
                        entities["checkout_date"] = ent.text
                elif "departure" in user_input or "flight" in user_input:
                    if not entities["departure_date"]:
                        entities["departure_date"] = ent.text
                    else:
                        entities["return_date"] = ent.text
                elif "pickup" in user_input or "rental car" in user_input:
                    if not entities["pickup_date"]:
                        entities["pickup_date"] = ent.text
                    else:
                        entities["dropoff_date"] = ent.text
            elif ent.label_ == 'ORG':
                entities["organization"] = ent.text  # Airlines, car rental companies, etc.
            elif ent.label_ == 'MONEY':
                entities["price"] = ent.text  # For price extraction
            elif ent.label_ == 'GPE':
                entities["country"] = ent.text  # Travel advisory country

        return entities

    def classify_intent(user_input):
        if "flight" in user_input.lower() or "fly" in user_input.lower():
            return "book_flight"
        elif "hotel" in user_input.lower():
            return "book_hotel"
        elif "advisory" in user_input.lower() or "travel advisory" in user_input.lower():
            return "travel_advisory"
        elif "hotel" in user_input.lower():
            return "rent_car"
        else:
            return "unknown"

    # Example of combining user input and retrieved context into a single prompt
    def prepare_prompt(user_input, context_data):
        context_text = "\n".join(context_data)
        prompt = f"You are a travel assistant. The user asked: '{user_input}'.\n\nHere is the information retrieved:\n{context_text}\n\nPlease assist the user based on this information."
        return prompt

    # Tokenize the prompt for GPT-2
    def tokenize_prompt(prompt):
        inputs = tokenizer(prompt, return_tensors='pt', max_length=1024, truncation=True)
        return inputs

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        user_input = data.get('message', '')
        # Get intent and entities
        intent = classify_intent(user_input)
        entities = extract_travel_entities(user_input)
        context_data = retrieve_travelinfo(intent,entities)
        response = generate_response(user_input,context_data)
        return jsonify({'response': response})
    

    @app.route('/flights')
    def get_flights():
        flights = Flight.query.all()
        flights_data = [{"airline": flight.airline, "departure": flight.departure, "destination": flight.destination} for flight in flights]
        return jsonify(flights=flights_data)
    
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)