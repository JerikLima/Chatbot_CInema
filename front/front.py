import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

# URL do seu servidor Rasa
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# Função para enviar mensagem para o Rasa e obter a resposta
def send_message(message):
    payload = {
        "sender": "user",
        "message": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(RASA_URL, json=payload, headers=headers)
    return response.json()

# Função para exibir a imagem no Streamlit
def display_image(image_url):
    if image_url.startswith("data:image"):
        image_base64 = image_url.split(",")[1]
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        st.image(image, caption='Filmes em Cartaz', use_column_width=True)  # Usar a largura da coluna
    else:
        st.warning("Formato de imagem não suportado.")

# Função para exibir os botões
def display_buttons(buttons, chat_index):
    num_buttons = len(buttons)
    for idx, button in enumerate(buttons):
        if st.button(button["title"], key=f"button_{chat_index}_{idx}"):
            response = send_message(button["payload"])
            st.session_state.history.append({"user": button["title"], "bot": response})

# Streamlit interface
st.title("Chatbot de Cinema")
st.write("Digite uma mensagem para começar a conversar com o bot.")

# Inicializar histórico da sessão para chat
if "history" not in st.session_state:
    st.session_state.history = []

# Entrada do usuário
user_input = st.text_input("Você: ", "")

if st.button("Enviar"):
    if user_input:
        response = send_message(user_input)
        st.session_state.history.append({"user": user_input, "bot": response})
        user_input = ""

# Exibir histórico do chat
for chat_index, chat in enumerate(st.session_state.history):
    st.markdown(f"**Você:** {chat['user']}")
    last_bot_response = ""
    for res in chat["bot"]:
        if "text" in res and res["text"] != last_bot_response:
            st.markdown(f"**Bot:** {res['text']}")
            last_bot_response = res["text"]
        if "attachment" in res:
            attachment = res["attachment"]
            if attachment["type"] == "image":
                display_image(attachment["content"])
        if "buttons" in res:
            display_buttons(res["buttons"], chat_index)

# Adicionar CSS customizado
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
        padding: 10px.
    }
    .stChatMessage {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0.
    }
    .userMessage {
        background-color: #dcf8c6;
        text-align: right.
    }
    .botMessage {
        background-color: #f1f0f0;
        text-align: left.
    }
    </style>
    """, unsafe_allow_html=True)
