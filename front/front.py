import streamlit as st
import requests
import json

# Define the URL of the Rasa server
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# Function to send a message to Rasa and get a response
def send_message(message):
    payload = {
        "sender": "user",
        "message": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(RASA_URL, data=json.dumps(payload), headers=headers)
    return response.json()

# Streamlit interface
st.title("Chatbot de Cinema")
st.write("Digite uma mensagem para começar a conversar com o bot.")


# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Você: ", "")

if st.button("Enviar"):
    if user_input:
        response = send_message(user_input)
        st.session_state.history.append({"user": user_input, "bot": response})
        user_input = ""

# Display chat history
for chat in st.session_state.history:
    st.write("Você: ", chat["user"])
    for res in chat["bot"]:
        st.write("Bot: ", res["text"])
