from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import load_dataset
import json
import os

# Load a pre-trained GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Load your travel dataset (assumed preprocessed and in JSON format)


def preprocess_data(file_path):
    current_dir = os.path.dirname(__file__)  # Get the current directory of the script
    data_dir = os.path.abspath(os.path.join(current_dir, '..','data'))  # Navigate one level up
    print(f'data_dir: {data_dir}')

    # Get the path to the directory one level up
    with open(data_dir+'/'+file_path, 'r') as file:
        data = json.load(file)
    
    processed_data = []
    for item in data:
        text = ""
        if item['type'] == 'flight_schedule':
            text = f"Flight Details:\nAirline: {item['data']['airline']}\nFlight Number: {item['data']['flight_number']}\nDeparture City: {item['data']['departure_city']}\nArrival City: {item['data']['arrival_city']}\nDeparture Time: {item['data']['departure_time']}\nArrival Time: {item['data']['arrival_time']}\nDuration: {item['data']['duration']}"
        elif item['type'] == 'hotel_availability':
            text = f"Hotel Availability:\nHotel Name: {item['data']['hotel_name']}\nLocation: {item['data']['location']}\nCheck-in Date: {item['data']['check_in_date']}\nCheck-out Date: {item['data']['check_out_date']}\nAvailable Rooms: {item['data']['available_rooms']}\nPrice per Night: {item['data']['price_per_night']}\nRating: {item['data']['rating']}"
        elif item['type'] == 'travel_advisory':
            text = f"Travel Advisory:\nCountry: {item['data']['country']}\nAdvisory: {item['data']['advisory']}\nDate Issued: {item['data']['date_issued']}"
        elif item['type'] == 'user_review':
            text = f"User Review:\nHotel Name: {item['data']['hotel_name']}\nLocation: {item['data']['location']}\nReviewer Name: {item['data']['reviewer_name']}\nReview Date: {item['data']['review_date']}\nRating: {item['data']['rating']}\nReview Text: {item['data']['review_text']}"
        elif item['type'] == 'travel_guide':
            attractions = ", ".join(item['data']['attractions'])
            restaurants = ", ".join(item['data']['recommended_restaurants'])
            text = f"Travel Guide:\nCity: {item['data']['city']}\nAttractions: {attractions}\nRecommended Restaurants: {restaurants}"
        
        processed_data.append(text)
    
    return processed_data


train_data = preprocess_data('train.json')
test_data = preprocess_data('test.json')

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01
)

# Initialize the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=test_data
)

# Train the model
trainer.train()

trainer.evaluate()

# Save the fine-tuned model
model.save_pretrained("./my-slm1")

# Save the tokenizer
tokenizer.save_pretrained("./my-slm1")
