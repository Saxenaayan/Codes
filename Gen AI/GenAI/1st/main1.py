



# from fastapi import FastAPI, HTTPException, status
# from pydantic import BaseModel
# import re
# import google.generativeai as genai
# import os
# import time


# app = FastAPI()

# # Set your Google API Key as an environment variable
# GOOGLE_API_KEY = "AIzaSyBmiDw7yTizDpWpXtrj3vBV_hTnyj_juR4"

# # Make sure your api key is initialized
# if not GOOGLE_API_KEY:
#     raise Exception("Error: Google API Key not found! Make sure that the environment variable GOOGLE_API_KEY is set!")

# genai.configure(api_key=GOOGLE_API_KEY)

# class UMLRequest(BaseModel):
#     description: str
#     model: str = "gemini-pro"  # Default value


# def generate_plantuml_gemini(text_description, model_name="gemini-pro"):
#     """
#     Converts a text description to PlantUML code using the Gemini API synchronously.

#     Args:
#         text_description: A string describing the system or relationship.
#         model_name: The name of the Gemini model to use.

#     Returns:
#         A string containing the PlantUML code or an error message.
#     """
#     try:
#         model = genai.GenerativeModel(model_name)

#         prompt = f"""You are an expert in generating PlantUML code from a text description, and providing insights for the system, including a brief description of the diagram.
#         Your goal is to generate both the PlantUML code, a brief explanation of the system described in the text description, and also a short description of what the diagram describes.
#         Include explainations also.
#         Here are some examples of what kind of input you should receive:
#             - Input: A user interacts with a web application which then interacts with a database
#             - PlantUML: 
#             @startuml
#                 actor User
#                 participant WebApplication
#                 database Database
#                 User -> WebApplication : interacts with
#                 WebApplication -> Database : reads/writes
#             @enduml
#             - Insights: This system describes a user interacting with a web application that reads and writes to a database.
#             - Diagram Description: This diagram illustrates the interaction between a user, a web application, and a database.
          
#         Based on that, generate the PlantUML, the insights, and the diagram description for this input:
#         Input: {text_description}
#         PlantUML:
#         """

#         start_time = time.time()
#         response = model.generate_content(prompt)
#         end_time = time.time()
#         print(f"Time taken to generate: {end_time - start_time}")
#         if response.text:
#             # We assume that the last block before @enduml is the block we want.
#             match = re.search(r'@startuml.*?@enduml', response.text, re.DOTALL)
#             if match:
#                 plantuml_code = match.group(0).strip()

#                 # Split based on @enduml to extract the prompt from the insights and the diagram description
#                 parts = response.text.split('@enduml')
#                 insights = parts[-1].strip() if len(parts) > 1 else ""
#                 diagram_desc_match = re.search(r'Diagram Description:\s*(.*?)$', insights, re.MULTILINE)
#                 diagram_description = diagram_desc_match.group(1).strip() if diagram_desc_match else ""
#                 # Remove the diagram description from the insights
#                 insights = re.sub(r'Diagram Description:\s*(.*?)$', '', insights, flags=re.MULTILINE).strip()

#                 return plantuml_code, insights, diagram_description
#             else:
#                 return "Could not find PlantUML code in the output from Gemini API.", "", ""
#         else:
#             return "Gemini API returned an empty response.", "", ""

#     except Exception as e:
#         return f"Error during processing: {e}", "", ""


# @app.post('/generate_uml')
# async def generate_uml(request: UMLRequest):

#     if not request.description:
#          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

#     # Step 1: Generate PlantUML code
#     plantuml_code, text_response, diagram_description = generate_plantuml_gemini(request.description, request.model)


#     if plantuml_code.startswith("Error"):
#       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)


#     return {
#         "uml_text": plantuml_code,
#         "text_response": text_response,
#         "diagram_description": diagram_description
#     }


# from fastapi import FastAPI, HTTPException, status
# from pydantic import BaseModel
# import re
# import google.generativeai as genai
# import os
# import time


# app = FastAPI()

# # Set your Google API Key as an environment variable
# GOOGLE_API_KEY = "AIzaSyBmiDw7yTizDpWpXtrj3vBV_hTnyj_juR4"

# # Make sure your api key is initialized
# if not GOOGLE_API_KEY:
#     raise Exception("Error: Google API Key not found! Make sure that the environment variable GOOGLE_API_KEY is set!")

# genai.configure(api_key=GOOGLE_API_KEY)

# class UMLRequest(BaseModel):
#     description: str
#     model: str = "gemini-pro"  # Default value


# def generate_plantuml_gemini(text_description, model_name="gemini-pro"):
#     """
#     Converts a text description to PlantUML code using the Gemini API synchronously.

#     Args:
#         text_description: A string describing the system or relationship.
#         model_name: The name of the Gemini model to use.

#     Returns:
#         A string containing the PlantUML code or an error message.
#     """
#     try:
#         model = genai.GenerativeModel(model_name)

#         prompt = f"""   You are an expert in generating PlantUML code from a text description.
#         Your goal is to generate only the PlantUML code. Also include some valuable insighs and explainations regarding diagram.
#         Here are some examples of what kind of input you should receive:
#             - Input: A user interacts with a web application which then interacts with a database
#             - PlantUML: 
#             @startuml
#                 actor User
#                 participant WebApplication
#                 database Database
#                 User -> WebApplication : interacts with
#                 WebApplication -> Database : reads/writes
#             @enduml
          
#         Based on that, generate the PlantUML, the insights and explainations to the diagram for this input:
#         Input: {text_description}
#         PlantUML:
#         """

#         start_time = time.time()
#         response = model.generate_content(prompt)
#         end_time = time.time()
#         print(f"Time taken to generate: {end_time - start_time}")
#         if response.text:
#             # We assume that the last block before @enduml is the block we want.
#             match = re.search(r'@startuml.*?@enduml', response.text, re.DOTALL)

#             if match:
#                 plantuml_code = match.group(0).strip()
#                 return plantuml_code
#             else:
#                 return "Could not find PlantUML code in the output from Gemini API."
#         else:
#             return "Gemini API returned an empty response."

#     except Exception as e:
#         return f"Error during processing: {e}"


# @app.post('/generate_uml')
# async def generate_uml(request: UMLRequest):

#     if not request.description:
#          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

#     # Step 1: Generate PlantUML code
#     plantuml_code = generate_plantuml_gemini(request.description, request.model)

#     if plantuml_code.startswith("Error"):
#       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)

#     return {
#         "uml_text": plantuml_code
        
#     }


#### Either you use code above this or the code Below

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import re
import google.generativeai as genai
import os
import time


app = FastAPI()

# Set your Google API Key as an environment variable
GOOGLE_API_KEY = "AIzaSyBmiDw7yTizDpWpXtrj3vBV_hTnyj_juR4"

# Make sure your api key is initialized
if not GOOGLE_API_KEY:
    raise Exception("Error: Google API Key not found! Make sure that the environment variable GOOGLE_API_KEY is set!")

genai.configure(api_key=GOOGLE_API_KEY)

class UMLRequest(BaseModel):
    description: str
    model: str = "gemini-pro"  # Default value


def generate_plantuml_gemini(text_description, model_name="gemini-pro"):
    """
    Converts a text description to PlantUML code using the Gemini API synchronously.

    Args:
        text_description: A string describing the system or relationship.
        model_name: The name of the Gemini model to use.

    Returns:
        A string containing the PlantUML code or an error message.
    """
    try:
        model = genai.GenerativeModel(model_name)

        prompt = f"""You are an expert in generating PlantUML code from a text description, and providing insights for the system, including a brief description of the diagram.
        Your goal is to generate both the PlantUML code, a brief explanation of the system described in the text description, and also a short description of what the diagram describes.
        Include Explainations to the diagram generated also.
        Here are some examples of what kind of input you should receive:
            - Input: A user interacts with a web application which then interacts with a database
            - PlantUML: 
            @startuml
                actor User
                participant WebApplication
                database Database
                User -> WebApplication : interacts with
                WebApplication -> Database : reads/writes
            @enduml
            - Insights: This system describes a user interacting with a web application that reads and writes to a database.
            - Diagram Description: This diagram illustrates the interaction between a user, a web application, and a database.
          
        Based on that, generate the PlantUML, the insights, and the diagram description for this input:
        Input: {text_description}
        PlantUML:
        """

        start_time = time.time()
        response = model.generate_content(prompt)
        end_time = time.time()
        print(f"Time taken to generate: {end_time - start_time}")
        if response.text:
            # We assume that the last block before @enduml is the block we want.
            match = re.search(r'@startuml.*?@enduml', response.text, re.DOTALL)
            if match:
                plantuml_code = match.group(0).strip()

                # Split based on @enduml to extract the prompt from the insights and the diagram description
                parts = response.text.split('@enduml')
                insights = parts[-1].strip() if len(parts) > 1 else ""
                diagram_desc_match = re.search(r'Diagram Description:\s*(.*?)$', insights, re.MULTILINE)
                diagram_description = diagram_desc_match.group(1).strip() if diagram_desc_match else ""
                # Remove the diagram description from the insights
                insights = re.sub(r'Diagram Description:\s*(.*?)$', '', insights, flags=re.MULTILINE).strip()

                return plantuml_code, insights, diagram_description
            else:
                return "Could not find PlantUML code in the output from Gemini API.", "", ""
        else:
            return "Gemini API returned an empty response.", "", ""

    except Exception as e:
        return f"Error during processing: {e}", "", ""


@app.post('/generate_uml')
async def generate_uml(request: UMLRequest):

    if not request.description:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

    # Step 1: Generate PlantUML code
    plantuml_code, text_response, diagram_description = generate_plantuml_gemini(request.description, request.model)


    if plantuml_code.startswith("Error"):
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)


    return {
        "uml_text": plantuml_code,
        "text_response": text_response,
        "diagram_description": diagram_description
    }






from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import re
import google.generativeai as genai
import os
import time


app = FastAPI()

# Set your Google API Key as an environment variable
GOOGLE_API_KEY = "AIzaSyBmiDw7yTizDpWpXtrj3vBV_hTnyj_juR4"

# Make sure your api key is initialized
if not GOOGLE_API_KEY:
    raise Exception("Error: Google API Key not found! Make sure that the environment variable GOOGLE_API_KEY is set!")

genai.configure(api_key=GOOGLE_API_KEY)

class UMLRequest(BaseModel):
    description: str
    model: str = "gemini-pro"  # Default value


def generate_plantuml_gemini(text_description, model_name="gemini-pro"):
    """
    Converts a text description to PlantUML code using the Gemini API synchronously.

    Args:
        text_description: A string describing the system or relationship.
        model_name: The name of the Gemini model to use.

    Returns:
        A string containing the PlantUML code or an error message.
    """
    try:
        model = genai.GenerativeModel(model_name)

        prompt = f"""You are an expert in generating PlantUML code from a text description, and providing insights for the system, including a brief description of the diagram.
        Your goal is to generate both the PlantUML code, a brief explanation of the system described in the text description, and also a short description of what the diagram describes.
        Include Explainations to the diagram generated also.
        Here are some examples of what kind of input you should receive:
            - Input: A user interacts with a web application which then interacts with a database
            - PlantUML: 
            @startuml
                actor User
                participant WebApplication
                database Database
                User -> WebApplication : interacts with
                WebApplication -> Database : reads/writes
            @enduml
            - Insights: This system describes a user interacting with a web application that reads and writes to a database.
            - Diagram Description: This diagram illustrates the interaction between a user, a web application, and a database.
         
        Here are other examples for different diagrams:
         
            - Input: User logs in using their username and password. System validates credentials and returns user details.
            - Diagram Type: Sequence Diagram
            - PlantUML: 
                @startuml
                actor User
                participant System
                User -> System: Login Request (username, password)
                activate System
                System -> System: Validate Credentials
                System --> User: User Details
                deactivate System
                @enduml
            - Insights: The sequence diagram illustrates the login process where a user interacts with the system for authentication.
            - Diagram Description: This is a sequence diagram that shows the steps involved in the user login process.

            - Input: A system for booking flights including options for search, booking, payment and confirmation
            - Diagram Type: Use Case Diagram
            - PlantUML: 
                @startuml
                left to right direction
                actor User
                rectangle FlightBooking {
                    User -- (Search Flights)
                    User -- (Book Flight)
                    User -- (Make Payment)
                    User -- (Get Confirmation)
                    (Search Flights) .> (Book Flight) : includes
                    (Book Flight) .> (Make Payment) : includes
                    (Make Payment) .> (Get Confirmation) : includes
                }
                @enduml
            - Insights: This describes a use case diagram for a flight booking system. This allows the user to search for flights, book them, make a payment and get a confirmation
            - Diagram Description: This is the use case diagram that illustrates how a user interacts with the flight booking system.


            - Input: A class with properties like name, author, pages and methods for read and write.
            - Diagram Type: Class Diagram
            - PlantUML: 
                @startuml
                class Book {
                    -String name
                    -String author
                    -int pages
                    +read()
                    +write()
                }
                @enduml
            - Insights: This is a class diagram that describes a book class with name, author and pages as attributes, and read and write as methods
            - Diagram Description: This is the class diagram that shows the different attributes and methods for a book class.

            - Input: Instances of a student class object with the attributes of name and registration number
            - Diagram Type: Object Diagram
            - PlantUML:
                @startuml
                object Student1 {{
                    name = "John Doe"
                    reg_number = 12345
                }}
                object Student2 {
                    name = "Jane Smith"
                    reg_number = 67890
                }
                @enduml
            - Insights: This diagram displays different student objects with their respective names and registration numbers.
            - Diagram Description: This is the object diagram which demonstrates examples of student objects and their attributes

            - Input: A system process where a customer order is received then validated and sent to fulfilment and the customer gets a notification
            - Diagram Type: Activity Diagram
            - PlantUML:
                @startuml
                (*) --> "Receive Order"
                --> "Validate Order"
                --> "Send to Fulfilment"
                --> "Notify Customer"
                --> (*)
                @enduml
            - Insights: This represents the flow of customer order processing starting from receiving the order to notifying the customer.
            - Diagram Description: This is the activity diagram illustrating the different steps involved in the order processing system.

             - Input: A system process where web application uses the frontend and the backend, as well as the database
             - Diagram Type: Component Diagram
            - PlantUML:
                @startuml
                [Frontend]
                [Backend]
                [Database]
                [Frontend] --> [Backend]
                [Backend] --> [Database]
                @enduml
            - Insights: This demonstrates a component diagram where the frontend utilizes the backend to communicate with a database.
            - Diagram Description: This component diagram shows the various components of a web application and their relationship

            - Input: A deployment diagram with a web server, application server and a database
            - Diagram Type: Deployment Diagram
            - PlantUML:
                @startuml
                node "Web Server" as web {
                    component "Web Application"
                }
                node "Application Server" as app {
                    component "Application Logic"
                }
                database "Database Server" as db {
                    database "Data Storage"
                }
                web -- app
                app -- db
                @enduml
             - Insights: This describes a deployment diagram which has a web server that communicates with an application server which then communicates with a database server.
             - Diagram Description: This diagram illustrates the deployment of the different servers for the web application.

            - Input: A door opening using a key and transitioning to the door opened state
            - Diagram Type: State Diagram
            - PlantUML:
                @startuml
                state Closed
                state Opened
                Closed --> Opened : key inserted
                Opened --> Closed : key removed
                @enduml
            - Insights: This demonstrates a state machine where the door goes through two states, one closed and another opened state depending on if the key is inserted.
            - Diagram Description: This state diagram illustrates the different states a door may be in depending on if the key is inserted.

            - Input: A process where a user starts an action, and the system responds, and then an event occurs to finish the action.
            - Diagram Type: Timing Diagram
            - PlantUML:
                @startuml
                @startuml
                
                
                |User |
                |#LightBlue|System|
                
                [->User: Start Action
                User -> System: Action Request
                activate System
                System -->> User: Response
                deactivate System
                [-->System: Event Occurs
                @enduml
            - Insights: This is a timing diagram that shows a user starting an action, and receiving a system response and when a specific event occurs.
            - Diagram Description: This diagram shows the different timings when a user starts an action and system completes an action.

        Based on that, generate the PlantUML, the insights, and the diagram description for this input:
        Input: {text_description}
        PlantUML:
        """

        start_time = time.time()
        response = model.generate_content(prompt)
        end_time = time.time()
        print(f"Time taken to generate: {end_time - start_time}")
        if response.text:
            # We assume that the last block before @enduml is the block we want.
            match = re.search(r'@startuml.*?@enduml', response.text, re.DOTALL)
            if match:
                plantuml_code = match.group(0).strip()

                # Split based on @enduml to extract the prompt from the insights and the diagram description
                parts = response.text.split('@enduml')
                insights = parts[-1].strip() if len(parts) > 1 else ""
                diagram_desc_match = re.search(r'Diagram Description:\s*(.*?)$', insights, re.MULTILINE)
                diagram_description = diagram_desc_match.group(1).strip() if diagram_desc_match else ""
                # Remove the diagram description from the insights
                insights = re.sub(r'Diagram Description:\s*(.*?)$', '', insights, flags=re.MULTILINE).strip()

                return plantuml_code, insights, diagram_description
            else:
                return "Could not find PlantUML code in the output from Gemini API.", "", ""
        else:
            return "Gemini API returned an empty response.", "", ""

    except Exception as e:
        return f"Error during processing: {e}", "", ""


@app.post('/generate_uml')
async def generate_uml(request: UMLRequest):

    if not request.description:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

    # Step 1: Generate PlantUML code
    plantuml_code, text_response, diagram_description = generate_plantuml_gemini(request.description, request.model)


    if plantuml_code.startswith("Error"):
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)


    return {
        "uml_text": plantuml_code,
        "text_response": text_response,
        "diagram_description": diagram_description
    }






## Fine Tuning the promt with more precise description of the diagram and the insights being given to the user




from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import re
import google.generativeai as genai
import os
import time

app = FastAPI()

# Set your Google API Key as an environment variable
GOOGLE_API_KEY = "AIzaSyBmiDw7yTizDpWpXtrj3vBV_hTnyj_juR4"

# Make sure your api key is initialized
if not GOOGLE_API_KEY:
    raise Exception("Error: Google API Key not found! Make sure that the environment variable GOOGLE_API_KEY is set!")

genai.configure(api_key=GOOGLE_API_KEY)

class UMLRequest(BaseModel):
    description: str
    model: str = "gemini-pro"  # Default value

def generate_plantuml_gemini(text_description, model_name="gemini-pro"):
    """
    Converts a text description to PlantUML code using the Gemini API synchronously.

    Args:
        text_description: A string describing the system or relationship.
        model_name: The name of the Gemini model to use.

    Returns:
        A string containing the PlantUML code or an error message.
    """
    try:
        model = genai.GenerativeModel(model_name)

        prompt = f"""
    You are an expert in generating PlantUML code from a text description, and providing accurate, concise insights about the system, along with a precise description of the generated diagram.

    Your goal is to:
    1.  Generate only the PlantUML code, ensuring it's syntactically correct and complete. Do not add any extra comments or text within the PlantUML code block.
    2.  Provide a brief, clear explanation of the system described in the input text (Insights).
    3.  Provide a concise description of what the generated diagram represents (Diagram Description).
    4.  Strictly follow the example format for each diagram type.
    5.  When the input does not clearly state the diagram type, make the best decision on the most appropriate diagram type to generate.

    Here are examples for different diagram types. Adhere strictly to these structures:

        - Input: A user interacts with a web application which then interacts with a database
        - Diagram Type: Component Diagram
        - PlantUML:
            @startuml
            [User]
            [WebApplication]
            [Database]
            User --> WebApplication
            WebApplication --> Database
            @enduml
        - Insights: This diagram illustrates a basic system architecture with a user interacting with a web application that reads and writes to a database.
        - Diagram Description: This is the component diagram that highlights the different components of the system and their relationships

        - Input: User logs in using their username and password. System validates credentials and returns user details.
        - Diagram Type: Sequence Diagram
        - PlantUML:
            @startuml
            actor User
            participant System
            User -> System: Login Request (username, password)
            activate System
            System -> System: Validate Credentials
            System --> User: User Details
            deactivate System
            @enduml
        - Insights: The sequence diagram illustrates the login process where a user sends a login request which the system validates before providing user details.
        - Diagram Description: This sequence diagram shows the interaction between the user and the system during login.

        - Input: A system for booking flights including options for search, booking, payment and confirmation
        - Diagram Type: Use Case Diagram
        - PlantUML:
            @startuml
            left to right direction
            actor User
            rectangle FlightBooking {{
                User -- (Search Flights)
                User -- (Book Flight)
                User -- (Make Payment)
                User -- (Get Confirmation)
                (Search Flights) -- (Book Flight) : includes
                (Book Flight) -- (Make Payment) : includes
                (Make Payment) -- (Get Confirmation) : includes
            }}
            @enduml
        - Insights: This describes the core functionalities of a flight booking system available to a user.
        - Diagram Description: This diagram represents the different actions a user performs when booking a flight.

        - Input: A class with properties like name, author, pages and methods for read and write.
        - Diagram Type: Class Diagram
        - PlantUML:
            @startuml
            class Book {{
                -String name
                -String author
                -int pages
                +read()
                +write()
            }}
            @enduml
        - Insights: This represents the data structure for a book with its attributes and methods.
        - Diagram Description: This is the class diagram of a book class showing its attributes and methods.

        - Input: Instances of a student class object with the attributes of name and registration number
        - Diagram Type: Object Diagram
        - PlantUML:
            @startuml
            object Student1 {{
                name = "John Doe"
                reg_number = 12345
            }}
            object Student2 {{
                name = "Jane Smith"
                reg_number = 67890
            }}
            @enduml
        - Insights: This diagram presents instances of the `Student` class with example data.
        - Diagram Description: This is the object diagram that shows examples of student objects and their attributes.

        - Input: A system process where a customer order is received, then validated, sent to fulfilment, and the customer gets a notification
        - Diagram Type: Activity Diagram
        - PlantUML:
            @startuml
            (*) --> "Receive Order"
            --> "Validate Order"
            --> "Send to Fulfilment"
            --> "Notify Customer"
            --> (*)
            @enduml
        - Insights: This demonstrates the process flow for how customer orders are managed by the system.
        - Diagram Description: This is the activity diagram that illustrates the sequence of activities in processing a customer order.

        - Input: A system process where a web application uses the frontend and the backend, as well as the database
        - Diagram Type: Component Diagram
        - PlantUML:
            @startuml
            [Frontend]
            [Backend]
            [Database]
            [Frontend] --> [Backend]
            [Backend] --> [Database]
            @enduml
        - Insights: This represents the standard structure of a web application with a clear separation between frontend, backend, and database.
        - Diagram Description: This diagram shows the different components of the web application and their relation.

        - Input: A deployment diagram with a web server, application server and a database
        - Diagram Type: Deployment Diagram
        - PlantUML:
            @startuml
            node "Web Server" as web {{
                component "Web Application"
            }}
            node "Application Server" as app {{
                component "Application Logic"
            }}
            database "Database Server" as db {{
                database "Data Storage"
            }}
            web -- app
            app -- db
            @enduml
         - Insights: This represents the deployment of a typical web application with dedicated servers for web, application logic, and data.
         - Diagram Description: This diagram illustrates how the different servers are deployed for a web application.

        - Input: A door opening using a key and transitioning to the door opened state
        - Diagram Type: State Diagram
        - PlantUML:
            @startuml
            state Closed
            state Opened
            Closed --> Opened : key inserted
            Opened --> Closed : key removed
            @enduml
        - Insights: This represents a simple state machine for a door with two distinct states based on a key insertion/removal.
        - Diagram Description: This is the state diagram for a door that illustrates how the door changes states depending on the key.

        - Input: A process where a user starts an action, the system responds, and then an event occurs to finish the action.
        - Diagram Type: Timing Diagram
        - PlantUML:
            @startuml
            
            
            |User |
            |#LightBlue|System|
            
            [->User: Start Action
            User -> System: Action Request
            activate System
            System -->> User: Response
            deactivate System
            [-->System: Event Occurs
            @enduml
        - Insights: This represents the timing of various events in a user-system interaction including a system response and a final event.
        - Diagram Description: This diagram displays the time and order of user-system interaction steps.


    Based on the input, generate the PlantUML code, insights, and diagram description in a structured manner.
    Input: {text_description}
    PlantUML:
    """
        start_time = time.time()
        response = model.generate_content(prompt)
        end_time = time.time()
        print(f"Time taken to generate: {end_time - start_time}")
        if response.text:
            # We assume that the last block before @enduml is the block we want.
            match = re.search(r'@startuml.*?@enduml', response.text, re.DOTALL)
            if match:
                plantuml_code = match.group(0).strip()

                # Split based on @enduml to extract the prompt from the insights and the diagram description
                parts = response.text.split('@enduml')
                insights = parts[-1].strip() if len(parts) > 1 else ""
                diagram_desc_match = re.search(r'Diagram Description:\s*(.*?)$', insights, re.MULTILINE)
                diagram_description = diagram_desc_match.group(1).strip() if diagram_desc_match else ""
                # Remove the diagram description from the insights
                insights = re.sub(r'Diagram Description:\s*(.*?)$', '', insights, flags=re.MULTILINE).strip()

                return plantuml_code, insights, diagram_description
            else:
                return "Could not find PlantUML code in the output from Gemini API.", "", ""
        else:
            return "Gemini API returned an empty response.", "", ""

    except Exception as e:
        return f"Error during processing: {e}", "", ""


@app.post('/generate_uml')
async def generate_uml(request: UMLRequest):
    if not request.description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

    # Step 1: Generate PlantUML code
    plantuml_code, text_response, diagram_description = generate_plantuml_gemini(request.description, request.model)

    if plantuml_code.startswith("Error"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)

    return {
        "uml_text": plantuml_code,
        "text_response": text_response,
        "diagram_description": diagram_description
    }