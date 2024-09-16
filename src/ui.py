import streamlit as st
import requests

# Define the URL of the Flask API
API_URL = "http://127.0.0.1:5000/chat"

st.title("Travel Chatbot")

# Create a text input box for user queries
user_input = st.text_input("Ask me anything about travel:")

if st.button("Send"):
    if user_input:
        # Send the user input to the Flask API
        response = requests.post(API_URL, json={"message": user_input})
        response_data = response.json()
        st.write("Chatbot:", response_data.get('response'))
    else:
        st.write("Please enter a message.")
