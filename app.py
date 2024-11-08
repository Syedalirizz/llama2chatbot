import streamlit as st
import requests

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
headers = {"Authorization": "Bearer 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"}  # Your Hugging Face token

def query_llama(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# UI Setup
st.set_page_config(page_title="LLaMA 2 Chatbot", page_icon="🤖")

# Title and Description
st.title("🤖 LLaMA 2 Chatbot")
st.write("An open-source chatbot powered by LLaMA 2 by Meta. Customize the conversation parameters and start chatting!")

# Sidebar for parameters
with st.sidebar:
    st.subheader("Models and Parameters")
    st.write("Adjust the model settings for a personalized experience.")
    
    model_type = st.selectbox("Choose a LLaMA model", ["LLaMA2-7B"], help="Currently limited to LLaMA2-7B model.")
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7, help="Controls randomness in the output.")
    top_p = st.slider("Top-p (Nucleus Sampling)", 0.1, 1.0, 0.9, help="Limits choices to tokens with top-p probability.")
    max_length = st.slider("Max Response Length", 20, 80, 50, help="Controls the length of responses.")

# Main chat interface
st.subheader("Chat")
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# User input and send button
user_input = st.text_input("Your message:", key="input", placeholder="Type a message and hit Enter...")

# Send button functionality
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Prepare input for the model
    model_input = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state["messages"]]
    
    # Query the model with parameters
    result = query_llama({
        "inputs": model_input,
        "parameters": {
            "temperature": temperature,
            "top_p": top_p,
            "max_length": max_length
        }
    })
    
    # Process response
    if result and isinstance(result, list):
        bot_response = result[0].get("generated_text", "I'm sorry, I couldn't process your request.")
        st.session_state["messages"].append({"role": "bot", "content": bot_response})
    else:
        st.write("There was an error processing the response.")
    st.text_input("Your message:", key="input", placeholder="Type a message and hit Enter...", value="", disabled=True)

# Display conversation history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.write(f"**You:** {msg['content']}")
    else:
        st.write(f"**Bot:** {msg['content']}")
