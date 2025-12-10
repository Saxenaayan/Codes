import streamlit as st
import requests
from plantuml import PlantUML
from IPython.display import Image, display
from io import BytesIO
import mimetypes

size = 0

# Initialize PlantUML
puml = PlantUML(url='http://www.plantuml.com/plantuml/img/')

st.set_page_config(layout="wide")

# Title and description
st.title("UML CHATBOT")
st.markdown("Chat with our UML generator! Provide descriptions, and the AI will return the generated PlantUML code and diagram.")

# Divides the screen into columns, and then column 2 into tabs
col1,col2 = st.columns(2)
with col2:
    tab1, tab2 = st.tabs(["UML Code","UML Map"])

user_messages = col1
ai_messages = col2

#Function to get Image bytes so it becomes downloadable as a png file
def get_image_bytes(img_url):
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type")
        if content_type is None:
            mime_type, _ = mimetypes.guess_type(img_url)
            if mime_type is None:
                mime_type = "image/png"  # Default
        else:
            mime_type = content_type

        return response.content, mime_type
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching image: {e}")
        return None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

#Function to dynamically present the UML image and code instead of appending them
def show_uml_code(size):
    if size == 0:
        return
    if st.session_state["messages"][-1]["role"] != "user":
        with ai_messages:
            with tab1:
                if "uml_code" in message:
                    st.markdown("Generated UML Code:")
                    st.code(message['uml_code'], language="plantuml")
            if "uml_image" in message:
                with tab2:
                    st.markdown("Generated UML Diagram:")
                    st.image(message['uml_image'])
                    image_bytes, mime_type = get_image_bytes(message['uml_img_url'])
                    if image_bytes and mime_type:
                        file_extension = mimetypes.guess_extension(mime_type)
                        if file_extension is None:
                            file_extension = ".png"

                        filename = "downloaded_image" + file_extension

                        st.download_button(
                            label="Download Image",
                            data=image_bytes,
                            file_name=filename,
                            mime=mime_type, 
                        )
                    else:
                        st.error("Could not download the image. Please check the URL.")


# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Stores chat messages



# Display chat history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        size += 1
        with user_messages:    
            st.markdown(f"**You:** {message['content']}")
    else:
        size += 1
        with user_messages:
            st.markdown(f"**AI:** {message['content']}")

show_uml_code(size) #running the uml code and image function above

with user_messages:
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
                response.raise_for_status()  
                response_data = response.json()

                uml_text = response_data.get("uml_text", "")
                    
                uml_image = None

                # Generate image from plantuml code if exists
                if uml_text:
                    try:
                        image_url = puml.get_url(uml_text)
                        image_response = requests.get(image_url)

                        if image_response.status_code == 200:
                            uml_image = image_response.content
                        else:
                            st.error(f"Failed to fetch UML diagram from PlantUML: HTTP {image_response.status_code}")
                    except Exception as e:
                        st.error(f"Failed to generate diagram: {e}")


                # Append AI's response to chat history
                ai_message = {"role": "ai", "content": ""}
                if uml_text:
                    ai_message["uml_code"] = uml_text
                if uml_image:
                    ai_message["uml_img_url"] = image_url
                    ai_message["uml_image"] = uml_image
                st.session_state["messages"].append(ai_message)



            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to UML generation service: {e}")
                
            except Exception as e:
                st.warning(f"Error: {e}")
        else:
            st.warning("Please enter a description for the diagram.")
