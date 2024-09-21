# how to access the model and tokenizer
from transformers import BertTokenizer, BertForSequenceClassification
from huggingface_hub import hf_hub_download
import pickle
import torch
import spacy
import re

# Load a pretrained spaCy NLP model (or transformers model for advanced use)
nlp = spacy.load("en_core_web_sm")

# Load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('Aishrock006/intent_model')

# Load the pre-trained BERT model for sequence classification
model = BertForSequenceClassification.from_pretrained('Aishrock006/intent_model')

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Move the model to the selected device (GPU or CPU)
model.to(device)

encoder_path = hf_hub_download(repo_id="Aishrock006/intent_model", filename="label_encoder.pkl")

with open(encoder_path, 'rb') as f:
  label_encoder = pickle.load(f)

# Get predictions
model.eval()

intents = {
        "BookFlight",
        "BookHotel",
        "RentCar",
        "CancelFlight",
        "CancelHotel",
        "CancelCar",
        "GetBooking",
        "SearchFlight",
        "SearchHotel",
        "SearchRentCar",
        "TravelAdvisory",
        "greeting",
        "goodbye",
        "thanks"
}

def classify_intent(user_input):
    print(f"user_input: {user_input}")
    #   model_intent =get_intent(user_input)
    #   if model_intent in intents:
    #       return model_intent
    intent = ""
    if re.search(rf"\bbook\b", user_input.lower()):
        intent="Book"
    elif "search" in user_input.lower():
        intent="Search"
        # Detect intent based on keywords
    elif "cancel" in user_input.lower():
        intent = 'Cancel'
    elif "get" in user_input.lower() or 'retrieve' in user_input.lower():
        intent = 'Get'
    else:
        return "unknown"
    
    if "flight" in user_input.lower() or "fly" in user_input.lower():
        return intent+"Flight"
    elif "hotel" in user_input.lower():
        return intent+"Hotel"
    elif "advisory" in user_input.lower() or "travel advisory" in user_input.lower():
        return "TravelAdvisory"
    elif "recommendations" in user_input.lower():
        return "TravelRecommendations"
    elif "hotel" in user_input.lower():
        return intent+"RentalCar"
    else:
        return "unknown"
 
def get_intent(user_input):
    # Tokenize new input
    new_text = [user_input]
    new_encodings = tokenizer(new_text, truncation=True, padding=True, max_length=64, return_tensors="pt")

    # Move the input encodings to the same device
    new_encodings = {key: val.to(device) for key, val in new_encodings.items()}

    with torch.no_grad():
        outputs = model(**new_encodings)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1)

    # Move predicted_class tensor to CPU and then convert to numpy
    predicted_class_cpu = predicted_class.cpu().numpy()

    # Convert back to label using label encoder
    predicted_intent = label_encoder.inverse_transform(predicted_class_cpu)
    print(f"Predicted intent for '{user_input}': {predicted_intent[0]}")

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
        "price": None,
        "traveller_names": [],  # To store traveller names,
        "booking_id": None,
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
        elif ent.label_ == 'PERSON':
            entities["traveller_names"].append(ent.text)  # Capture travellers' names
        elif ent.label_ == 'GPE':
            entities["country"] = ent.text  # Travel advisory country
        elif ent.label_ == 'CARDINAL' and ent.text.isdigit():  # Booking ID
            entities['booking_id'] = int(ent.text)

    print(f"entities: {entities}")
    return entities