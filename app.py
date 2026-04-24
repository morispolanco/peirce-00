import streamlit as st
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Chatbot Abductivo", layout="wide")

st.title("🧠 Chatbot Abductivo Universal")
st.caption("Responde, explica y genera hipótesis cuando es necesario")

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
# HISTORIAL
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
Eres un asistente inteligente que aplica la lógica abductiva de Charles Sanders Peirce cuando es necesario.

Reglas:

1. Si la pregunta es simple → responde directamente.
2. Si hay un problema, anomalía o incertidumbre:
   - Identifica el hecho sorprendente
   - Genera hipótesis
   - Selecciona la más plausible
   - Explica por qué
   - Sugiere qué verificar

Sé claro, lógico y útil. No fuerces abducción si no es necesario.
"""
        }
    ]

# -----------------------------
# MOSTRAR CHAT
# -----------------------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# INPUT
# -----------------------------
user_input = st.chat_input("Escribe tu pregunta...")

if user_input:

    # Mostrar usuario
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Respuesta
    with st.chat_message("assistant"):
        with st.spinner("Razonando..."):

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=st.session_state.messages,
                    temperature=0.7
                )

                reply = response.choices[0].message.content

            except Exception as e:
                reply = "⚠️ Error al procesar la respuesta"

            st.write(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

# -----------------------------
# LIMPIAR CHAT
# -----------------------------
if st.sidebar.button("🧹 Limpiar conversación"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
Eres un asistente que aplica lógica abductiva cuando es necesario.
"""
        }
    ]
    st.rerun()
