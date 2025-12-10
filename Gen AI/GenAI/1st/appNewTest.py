import streamlit as st
import requests
from plantuml import PlantUML
from IPython.display import Image, display

# Initialize PlantUML
puml = PlantUML(url='http://www.plantuml.com/plantuml/img/')

# Initialize session state for chat history and edited UML code
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "edited_uml_code" not in st.session_state:
    st.session_state["edited_uml_code"] = ""
if "uml_image" not in st.session_state:
    st.session_state["uml_image"] = None

# Title and description
st.title("UML CHATBOT")
st.markdown("Chat with our UML generator! Provide descriptions, and the AI will return the generated PlantUML code and diagram.")

# Function to generate and display UML Diagram
def generate_and_display_uml(uml_code):
    if uml_code:
        try:
            image_url = puml.get_url(uml_code)
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                st.session_state["uml_image"] = image_response.content
            else:
                st.error(f"Failed to fetch UML diagram from PlantUML: HTTP {image_response.status_code}")
        except Exception as e:
            st.error(f"Failed to generate diagram: {e}")
    else:
        st.session_state["uml_image"] = None


# Display chat history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**AI:** {message['content']}")
        if "uml_code" in message:
            st.session_state["edited_uml_code"] = st.text_area("Generated UML Code (Editable)",
                                       value=message['uml_code'],
                                       key="code_editor",
                                       height=200)

        if st.button("Update Diagram", key=f"update_{message['content']}"):
            generate_and_display_uml(st.session_state["edited_uml_code"])
           
        if st.session_state["uml_image"] is not None:
            st.markdown("Generated UML Diagram:")
            st.image(st.session_state["uml_image"])

# Text input for the user
user_input = st.text_input("Type your message here:")

# Dropdown for model selection
model_name = st.selectbox(
    "Choose a model for generating UML descriptions:",
    ["gemini-pro", "gemini-pro-vision", "gemini-1.0-pro", "gemini-1.0-pro-001"],
    index = 0 # Default model set to "gemini-pro"
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
            response.raise_for_status()  
            response_data = response.json()

            uml_text = response_data.get("uml_text", "")
            
            uml_image = None
            if uml_text:
                generate_and_display_uml(uml_text)


            # Append AI's response to chat history
            ai_message = {"role": "ai", "content": ""}
            if uml_text:
                 ai_message["uml_code"] = uml_text
            st.session_state["messages"].append(ai_message)

        except requests.exceptions.RequestException as e:
           st.error(f"Failed to connect to UML generation service: {e}")
        except Exception as e:
            st.warning(f"Error: {e}")
    else:
        st.warning("Please enter a description for the diagram.")