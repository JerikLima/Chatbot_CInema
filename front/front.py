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

# Function to display bot response buttons
def display_buttons(buttons, chat_index):
    num_buttons = len(buttons)
    half = (num_buttons + 1) // 2  # Calculate the middle index for splitting buttons into two rows

    # Display the first row of buttons
    row1 = st.columns(half)
    for idx, button in enumerate(buttons[:half]):
        button_key = f"button_{chat_index}_{idx}"
        with row1[idx]:
            if st.button(button["title"], key=button_key):
                response = send_message(button["payload"])
                st.session_state.history.append({"user": button["title"], "bot": response})

    # Display the second row of buttons
    row2 = st.columns(num_buttons - half)
    for idx, button in enumerate(buttons[half:]):
        button_key = f"button_{chat_index}_{half + idx}"
        with row2[idx]:
            if st.button(button["title"], key=button_key):
                response = send_message(button["payload"])
                st.session_state.history.append({"user": button["title"], "bot": response})

# Display chat history
for chat_index, chat in enumerate(st.session_state.history):
    st.markdown(f"**Você:** {chat['user']}")
    last_bot_response = ""  # Initialize a variable to store the last bot response
    for res in chat["bot"]:
        if res["text"] != last_bot_response:
            st.markdown(f"**Bot:** {res['text']}")
            if "buttons" in res:
                display_buttons(res["buttons"], chat_index)
            last_bot_response = res["text"]  # Update the last bot response

# Add custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 12px;
        margin: 2px; /* Margin between buttons */
        cursor: pointer;
        width: auto; /* Adjust width automatically */
    }
    .stTextInput>div>input {
        font-size: 18px;
        padding: 10px;
    }
    .stChatMessage {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .userMessage {
        background-color: #dcf8c6;
        text-align: right;
    }
    .botMessage {
        background-color: #f1f0f0;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)
