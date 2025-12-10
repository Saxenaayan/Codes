# import streamlit as st
# import requests
# from plantuml import PlantUML
# from IPython.display import Image, display
# from io import BytesIO
# import mimetypes

# size = 0

# # Initialize PlantUML
# puml = PlantUML(url='http://www.plantuml.com/plantuml/img/')

# st.set_page_config(layout="centered")

# # Title and description
# st.title("CHATBOT")

# tab1,tab2 = st.tabs(["Diagram", "Code"])

# #Function to get Image bytes so it becomes downloadable as a png file
# def get_image_bytes(img_url):
#     try:
#         response = requests.get(img_url, stream=True)
#         response.raise_for_status()

#         content_type = response.headers.get("Content-Type")
#         if content_type is None:
#             mime_type, _ = mimetypes.guess_type(img_url)
#             if mime_type is None:
#                 mime_type = "image/png"  # Default
#         else:
#             mime_type = content_type

#         return response.content, mime_type
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching image: {e}")
#         return None, None
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return None, None


# def generate_and_display_uml(uml_code):
#     if uml_code:
#         try:
#             image_url = puml.get_url(uml_code)
#             image_response = requests.get(image_url)

#             if image_response.status_code == 200:
#                 uml_image = image_response.content
#                 with tab1:
#                     st.markdown("Generated Diagram:")
#                     st.image(uml_image)
#                     st.write(st.session_state["diagram_description"])
#                     image_bytes, mime_type = get_image_bytes(image_url)
#                     if image_bytes and mime_type:
#                         file_extension = mimetypes.guess_extension(mime_type)
#                         if file_extension is None:
#                             file_extension = ".png"

#                         filename = "downloaded_image" + file_extension

#                         st.download_button(
#                             label="Download Image",
#                             data=image_bytes,
#                             file_name=filename,
#                             mime=mime_type, 
#                         )
#                     else:
#                         st.error("Could not download the image. Please check the URL.")
#             else:
#                 st.error(f"Failed to fetch UML diagram from PlantUML: HTTP {image_response.status_code}")
#         except Exception as e:
#             st.error(f"Failed to generate diagram: {e}")

# def uml_code_popover(uml_code):
#     if uml_code:
#         with tab2:
#             st.markdown("Generated Code:")
#             st.session_state["uml_code"] = st.text_area("Generated Code (Editable)",
#                                                         value=uml_code,
#                                                         key=f"code_editor_{message['content']}",
#                                                         height=200)

# if "messages" not in st.session_state:
#     st.session_state["messages"] = []  # Stores chat messages
# if "uml_code" not in st.session_state:
#     st.session_state["uml_code"] = ""
# if "uml_image" not in st.session_state:
#     st.session_state["uml_image"] = None
# if "uml_img_url" not in st.session_state:
#     st.session_state["uml_img_url"] = None
# if "diagram_description" not in st.session_state:
#     st.session_state["diagram_description"] = ""

# with st.sidebar:

#     st.markdown("Chat with our UML generator! Provide descriptions, and the AI will return the generated PlantUML code and diagram.")

    
#     # Dropdown for model selection
#     model_name = st.selectbox(
#         "Choose a model for generating UML descriptions:",
#         ["gemini-pro", "gemini-pro-vision", "gemini-1.0-pro", "gemini-1.0-pro-001"],
#         index = 0
#     )

#     messages = st.container(height = 500)
#     if prompt := st.chat_input("Type your message here"):
#         st.session_state["messages"].append({"role" : "user","content" : prompt})
#         api_url = "http://127.0.0.1:8000/generate_uml"
#         payload = {
#             "description": prompt,
#             "model": model_name
#         }
        
#         try:
#             response = requests.post(api_url,json=payload)
#             response.raise_for_status()
#             response_data = response.json()

#             uml_text = response_data.get("uml_text", "")
#             text_response = response_data.get("text_response","")
#             diagram_description = response_data.get("diagram_description","")
                    
#             uml_image = None



#                 # Append AI's response to chat history
#             # Append AI's response to chat history
#             ai_message = {"role": "ai", "content": ""}
#             if uml_text:
#                 ai_message["uml_code"] = uml_text
#                 st.session_state["uml_code"] = uml_text
#                 st.session_state["messages"].append({"role":"AI","content":text_response})
#                 st.session_state["diagram_description"] = diagram_description
            
#             if uml_image:
#                 ai_message["uml_image"] = uml_image
#                 st.session_state["uml_image"] = uml_image

#         except requests.exceptions.RequestException as e:
#             st.error(f"Failed to connect to UML generation service: {e}")
                
#         except Exception as e:
#             st.warning(f"Error: {e}")
#     else:
#         st.warning("Please enter a description for the diagram.")
    
#     for message in st.session_state["messages"]:
#         if message["role"] == "user":
#             messages.chat_message("user").write(message["content"])
#         else:
#             messages.chat_message("assistant").write(message["content"])

# uml_code_popover(st.session_state["uml_code"])

# generate_and_display_uml(st.session_state["uml_code"])










#  Best of Both worlds






import streamlit as st
import requests
from plantuml import PlantUML
import mimetypes
from io import BytesIO

size = 0

# Initialize PlantUML
puml = PlantUML(url='http://www.plantuml.com/plantuml/img/')

st.set_page_config(layout="centered")

# Title and description
st.title("CHATBOT")

tab1, tab2 = st.tabs(["Diagram", "Code"])


# Function to get Image bytes so it becomes downloadable as a png file
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


def generate_and_display_uml(uml_code):
    if uml_code:
        try:
            image_url = puml.get_url(uml_code)
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                uml_image = image_response.content
                with tab1:
                    st.markdown("Generated Diagram:")
                    st.image(uml_image)
                    st.write(st.session_state["diagram_description"])
                    image_bytes, mime_type = get_image_bytes(image_url)
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
            else:
                st.error(f"Failed to fetch UML diagram from PlantUML: HTTP {image_response.status_code}")
        except Exception as e:
            st.error(f"Failed to generate diagram: {e}")


def uml_code_popover(uml_code):
    if uml_code:
        with tab2:
            st.markdown("Generated Code:")
            st.session_state["uml_code"] = st.text_area("Generated Code (Editable)",
                                                        value=uml_code,
                                                        key=f"code_editor_{st.session_state.get('latest_message', '')}",
                                                        height=200)
            if st.button("Update Diagram", key=f"update_button_{st.session_state.get('latest_message', '')}"):
                generate_and_display_uml(st.session_state["uml_code"])


if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Stores chat messages
if "uml_code" not in st.session_state:
    st.session_state["uml_code"] = ""
if "uml_image" not in st.session_state:
    st.session_state["uml_image"] = None
if "uml_img_url" not in st.session_state:
    st.session_state["uml_img_url"] = None
if "diagram_description" not in st.session_state:
    st.session_state["diagram_description"] = ""
if "latest_message" not in st.session_state:
    st.session_state["latest_message"] = ""

with st.sidebar:
    st.markdown(
        "Chat with our UML generator! Provide descriptions, and the AI will return the generated PlantUML code and diagram.")

    # Dropdown for model selection
    model_name = st.selectbox(
        "Choose a model for generating UML descriptions:",
        ["gemini-pro", "gemini-pro-vision", "gemini-1.0-pro", "gemini-1.0-pro-001"],
        index=0
    )

    messages = st.container(height=500)
    if prompt := st.chat_input("Type your message here"):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.session_state["latest_message"] = prompt
        api_url = "http://127.0.0.1:8000/generate_uml"
        payload = {
            "description": prompt,
            "model": model_name
        }

        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            response_data = response.json()

            uml_text = response_data.get("uml_text", "")
            text_response = response_data.get("text_response", "")
            diagram_description = response_data.get("diagram_description", "")

            uml_image = None

            # Append AI's response to chat history
            ai_message = {"role": "ai", "content": ""}
            if uml_text:
                ai_message["uml_code"] = uml_text
                st.session_state["uml_code"] = uml_text
                st.session_state["messages"].append({"role": "AI", "content": text_response})
                st.session_state["diagram_description"] = diagram_description

            if uml_image:
                ai_message["uml_image"] = uml_image
                st.session_state["uml_image"] = uml_image

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to UML generation service: {e}")

        except Exception as e:
            st.warning(f"Error: {e}")
    else:
        st.warning("Please enter a description for the diagram.")
    
    if st.button("Generate Flowchart"):
      api_url = "http://127.0.0.1:8000/generate_flowchart"
      payload = {
            "description": st.session_state["latest_message"],
            "model": model_name
        }
      
      try:
            response = requests.post(api_url,json=payload)
            response.raise_for_status()
            response_data = response.json()

            uml_text = response_data.get("uml_text", "")
            text_response = response_data.get("text_response","")
            diagram_description = response_data.get("diagram_description","")
                    
            uml_image = None



                # Append AI's response to chat history
            # Append AI's response to chat history
            ai_message = {"role": "ai", "content": ""}
            if uml_text:
                ai_message["uml_code"] = uml_text
                st.session_state["uml_code"] = uml_text
                st.session_state["messages"].append({"role":"AI","content":text_response})
                st.session_state["diagram_description"] = diagram_description
            
            if uml_image:
                ai_message["uml_image"] = uml_image
                st.session_state["uml_image"] = uml_image

      except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to Flowchart generation service: {e}")
                
      except Exception as e:
            st.warning(f"Error: {e}")
    if instruction := st.chat_input("Modify the diagram (text-based)"):
        st.session_state["messages"].append({"role": "user", "content": instruction})
        api_url = "http://127.0.0.1:8000/modify_uml"
        payload = {
            "uml_code": st.session_state["uml_code"],
            "diagram_instruction": instruction,
            "model": model_name
        }
        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            response_data = response.json()

            uml_text = response_data.get("uml_text", "")
            text_response = response_data.get("text_response","")
            diagram_description = response_data.get("diagram_description","")
            uml_image = None

            # Append AI's response to chat history
            ai_message = {"role": "ai", "content": ""}
            if uml_text:
                ai_message["uml_code"] = uml_text
                st.session_state["uml_code"] = uml_text
                st.session_state["messages"].append({"role": "AI", "content": text_response})
                st.session_state["diagram_description"] = diagram_description
            
            if uml_image:
                ai_message["uml_image"] = uml_image
                st.session_state["uml_image"] = uml_image

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to UML modification service: {e}")
        except Exception as e:
            st.warning(f"Error: {e}")

    for message in st.session_state["messages"]:
        if message["role"] == "user":
            messages.chat_message("user").write(message["content"])
        else:
            messages.chat_message("assistant").write(message["content"])

uml_code_popover(st.session_state["uml_code"])

generate_and_display_uml(st.session_state["uml_code"])