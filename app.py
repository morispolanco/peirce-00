import streamlit as st
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Chatbot General", layout="wide")

st.title("🤖 Chatbot Inteligente")
st.caption("Pregúntame lo que quieras")

# -----------------------------
# OPENROUTER
# -----------------------------
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Falta API KEY")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# -----------------------------
# MODELOS
# -----------------------------
modelo = st.sidebar.selectbox(
    "Modelo",
    [
        "openai/gpt-4o-mini",
        "openai/gpt-4o",
        "anthropic/claude-sonnet-4.6",
        "meta-llama/llama-3.1-70b-instruct"
    ]
)

# -----------------------------
# HISTORIAL
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres un asistente útil, claro y preciso."}
    ]

# -----------------------------
# MOSTRAR CHAT
# -----------------------------
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# -----------------------------
# INPUT USUARIO
# -----------------------------
user_input = st.chat_input("Escribe tu pregunta...")

# -----------------------------
# RESPUESTA
# -----------------------------
if user_input:
    # Mostrar mensaje usuario
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):

            try:
                response = client.chat.completions.create(
                    model=modelo,
                    messages=st.session_state.messages,
                    temperature=0.7
                )

                reply = response.choices[0].message.content

            except Exception as e:
                reply = f"❌ Error: {str(e)}"

            st.write(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

# -----------------------------
# BOTONES EXTRA
# -----------------------------
st.sidebar.markdown("---")

if st.sidebar.button("🧹 Limpiar conversación"):
    st.session_state.messages = [
        {"role": "system", "content": "Eres un asistente útil, claro y preciso."}
    ]
    st.rerun()
