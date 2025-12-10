import streamlit as st
import requests

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Stores chat messages

# Title and description
st.title("UML Chat (Text Only)")
st.markdown("Chat with our UML generator! Provide descriptions, and the AI will return the generated PlantUML code.")

# Display chat history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**AI:** {message['content']}")

# Text input for the user
user_input = st.text_input("Type your message here:")

# Dropdown for model selection
model_name = st.selectbox(
    "Choose a model for generating UML descriptions:",
    ["gemini-pro"]
)

# Button to send message
if st.button("Send"):
    if user_input.strip():
        # Append user's message to chat history
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Send input to the backend API
        api_url = "http://127.0.0.1:8000/generate_uml"
        payload = {
            "description": user_input,
            "model": model_name
        }

        try:
            response = requests.post(api_url, json=payload)
            response_data = response.json()
            if response.status_code == 200:
                uml_text = response_data.get("uml_text", "")

                # Append AI's response to chat history
                st.session_state["messages"].append({"role": "ai", "content": uml_text})

                # Show the UML code
                if uml_text:
                   st.markdown("Generated UML Code:")
                   st.code(uml_text, language="plantuml")
            else:
                st.warning(f"Error: {response_data.get('error', 'Unknown error occurred.')}")
        except Exception as e:
            st.error(f"Failed to connect to UML generation service: {e}")
    else:
        st.warning("Please enter a description for the diagram.")