from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from db_models import db, Flight # Import the db instance from models
from mock_data import create_mock_data
from search_service import retrieve_travelinfo
from booking_service import create_booking
from intent_entities import classify_intent, extract_travel_entities
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def create_app():
        # Check if GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load a pre-trained GPT-2 model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("Aishrock006/chat_model")
    #tokenizer = GPT2Tokenizer.from_pretrained("C:/Users/krish/Downloads/chat_model2")
    
    # Set a separate padding token to avoid warnings
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        # Step 4: Load pre-trained GPT-2 model
    model = GPT2LMHeadModel.from_pretrained("Aishrock006/chat_model")
    #model = GPT2Tokenizer.from_pretrained("C:/Users/krish/Downloads/chat_model2")

    # Resize the model embeddings to accommodate the new [PAD] token
    model.resize_token_embeddings(len(tokenizer))

    model.to(device)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_info.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    session = {}
    session['user_id'] = str(uuid.uuid4())
    session['chat_history'] = []

    lemmatizer = WordNetLemmatizer()
        
    # Download stopwords and wordnet for lemmatization
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    stop_words = set(stopwords.words('english'))
   
    # Initialize the app with SQLAlchemy
    with app.app_context():
        # Check if the SQLite database file exists (for SQLite only)
        if not os.path.exists(app.instance_path+'/travel_info.db'):
            print("Database does not exist, creating...")
            # Create all tables
            db.create_all()
            create_mock_data()
            print("Database and tables created.")
        else:
            print("Database already exists.")

    def preprocess_text(text):
        # Convert to lowercase
        text = text.lower()

        # Remove special characters and numbers
        text = re.sub(r'[^a-z\s]', '', text)

        # Tokenize the text
        words = text.split()

        # Remove stopwords and lemmatize
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

        # Join the words back into a single string
        return ' '.join(words)
    
    # def generate_response(prompt, device):
    #     # Tokenize input prompt, generating both input_ids and attention_mask
    #     inputs = tokenizer(preprocess_text(prompt), return_tensors='pt', padding=True).to(device)
        
    #     input_ids = inputs['input_ids']
    #     attention_mask = inputs['attention_mask']

    #     # Move the model to the same device
    #     model.to(device)

    #     # Generate a response with strict control over length and sampling
    #     outputs = model.generate(
    #         input_ids,
    #         attention_mask=attention_mask,  # Use the attention mask to handle padding
    #         max_length=50,  # Restrict the length of the response
    #         num_return_sequences=1,  # Ensure only one response is generated
    #         temperature=0.7,  # Lower temperature for more deterministic responses
    #         top_k=10,  # Limit the number of tokens considered
    #         top_p=0.85,  # Nucleus sampling with a cumulative probability
    #         repetition_penalty=1.2,  # Penalize repeated phrases
    #         pad_token_id=tokenizer.eos_token_id,  # EOS token for padding
    #         do_sample=True  # Enable sampling for more diverse responses
    #     )

    #     # Decode the response
    #     response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    #     # Optionally, return only the first reply from the agent
    #     if "agent" in response:
    #         response = response.split("agent")[-1].strip()  # Keep only the agent's first reply

    #     return response

    #Generate a response using GPT-2
    def generate_response(context_data):
        # Prepare and tokenize the prompt
        ctx = " ".join(context_data)
        # Truncate the string to the last 1000 characters
        prompt = f"{ctx} Agent:"
        print(f"prompt: {prompt}")
        inputs = tokenizer.encode(prompt, return_tensors='pt').to(device)

        # Generate a response with strict control over length and sampling
        outputs = model.generate(
        inputs,
        max_new_tokens=30, # Restrict the length of the response to one reply
        num_return_sequences=1, # Ensure only one response is generated
        temperature=0.5, # Lower temperature for more deterministic responses
        top_k=10, # Limit the number of tokens considered
        top_p=0.85, # Nucleus sampling with a cumulative probability
        repetition_penalty=1.2, # Penalize repeated phrases
        pad_token_id=tokenizer.eos_token_id, # EOS token for padding
        do_sample=False # Disable sampling for a deterministic output
        )

        # Decode the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.replace("'", "").replace('"', '')
        print(f"response: {response}")

        # Return only the first reply from the agent
        # Ensure that it stops after the first "Agent:" prompt
        if "Agent:" in response:
            response = response.split("Agent:")[-1].strip() # Keep only the agent's first reply

        # Alternatively, stop at the first period if it's part of the sentence structure
        response = response.split(".")[0].strip() + "," # Stop at first full stop
        return response

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        user_input = data.get('message', '')
        # Get intent and entities
        intent = classify_intent(user_input)
        print(f"intent: {intent}")
        entities = extract_travel_entities(user_input)
        context_data=""
        if(intent.startswith("Search") or intent.startswith("Travel")):
            context_data = retrieve_travelinfo(intent,entities,session['user_id'])
        elif(intent.startswith("Book") or intent.startswith("Cancel") or intent.startswith("Get")):
            context_data = create_booking(intent,entities,session['user_id'])
        print(f"retrieved context_info from db: {context_data}")
         # Add the user's message to the chat history
        session['chat_history'].append(f"Customer: {user_input}")
        if context_data:
            # Add the bot's response to the chat history
            session['chat_history'].append(f"agent: {context_data}")
        response = generate_response(session['chat_history'])
        # Add the bot's response to the chat history
        session['chat_history'].append(f"agent: {response}")
        session['chat_history'] = session['chat_history'][-10:]
        return jsonify({'response': response})
    
    @app.route('/flights')
    def get_flights():
        flights = Flight.query.all()
        flights_data = [{"airline": flight.airline, "departure": flight.departure, "destination": flight.destination, "departure_time": flight.departure_time} for flight in flights]
        return jsonify(flights=flights_data)
    
    @app.route('/get_history', methods=['GET'])
    def get_history():
        # Retrieve the chat history from the session
        chat_history = session['chat_history']
        print(f"chat_history: {chat_history}")
        return jsonify(chat_history)
    
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)