import streamlit as st
import ollama

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Custom CSS for enhanced UI
st.markdown("""
<style>
/* Main container styling */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
/* Chat message styling */
.stChatMessage {
    padding: 1.5rem;
    border-radius: 20px;
    margin: 0.8rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    max-width: 80%;
}
/* User message specific styling */
[data-testid="stChatMessage"]:has(div:contains("user")) {
    background: #ffffff;
    margin-left: auto;
    border: 1px solid #e0e0e0;
}
/* Bot message specific styling */
[data-testid="stChatMessage"]:has(div:contains("assistant")) {
    background: #6c5ce7;
    color: white;
    margin-right: auto;
    border: 1px solid #5b4bc4;
}
/* Chat input styling */
.stTextInput > div > div > input {
    border-radius: 25px;
    padding: 1rem 2rem;
    font-size: 1rem;
    border: 2px solid #6c5ce7;
}
/* Hover effects */
.stChatMessage:hover {
    transform: translateY(-2px);
    transition: transform 0.2s ease;
}
/* Custom title styling */
.title-container {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(90deg, #6c5ce7, #4b3cad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# Header with gradient text
st.markdown("""
<div class="title-container">
    <h1 style='font-size: 2.5em; margin: 0;'>My First Chat Assistant</h1>
    <p style='color: #6c5ce7; margin: 0;'>Made by Four Zero Productions</p>
</div>
""", unsafe_allow_html=True)

# Display conversation history
for message in st.session_state.conversation_history:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.spinner("Generating response..."):
        response = ollama.chat(
            model="qwen2.5:0.5b",
            messages=st.session_state.conversation_history,
            stream=False
        )
    
    # Get bot response
    bot_response = response["message"]["content"]
    
    # Add to history
    st.session_state.conversation_history.append({"role": "assistant", "content": bot_response})
    st.rerun()