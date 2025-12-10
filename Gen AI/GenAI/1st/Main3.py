

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

#         prompt = f"""
#     You are an expert in generating PlantUML diagrams from textual descriptions. Your task is to create accurate PlantUML code that precisely represents the system described. Alongside the code, provide a clear explanation of the system, detailing its components, their interactions, and overall functionality. Additionally, include a concise summary of what the diagram depicts and its purpose. To enhance understanding, highlight the key elements and relationships within the diagram, ensuring clarity and relevance to the given description.

#     Your goal is to:
#     1.  Generate only the PlantUML code, ensuring it's syntactically correct and complete. Do not add any extra comments or text within the PlantUML code block.
#     2.  Provide a brief, clear explanation of the system described in the input text (Insights).
#     3.  Provide a concise description of what the generated diagram represents (Diagram Description).
#     4.  Strictly follow the example format for each diagram type.
#     5.  When the input does not clearly state the diagram type, make the best decision on the most appropriate diagram type to generate.

#     Here are examples for different diagram types. Adhere strictly to these structures:

#         - Input: A user interacts with a web application which then interacts with a database
#         - Diagram Type: Component Diagram
#         - PlantUML:
#             @startuml
#             [User]
#             [WebApplication]
#             [Database]
#             User --> WebApplication
#             WebApplication --> Database
#             @enduml
#         - Insights: This diagram illustrates a basic system architecture with a user interacting with a web application that reads and writes to a database.
#         - Diagram Description: This is the component diagram that highlights the different components of the system and their relationships

#         - Input: User logs in using their username and password. System validates credentials and returns user details.
#         - Diagram Type: Sequence Diagram
#         - PlantUML:
#             @startuml
#             actor User
#             participant System
#             User -> System: Login Request (username, password)
#             activate System
#             System -> System: Validate Credentials
#             System --> User: User Details
#             deactivate System
#             @enduml
#         - Insights: The sequence diagram illustrates the login process where a user sends a login request which the system validates before providing user details.
#         - Diagram Description: This sequence diagram shows the interaction between the user and the system during login.

#         - Input: A system for booking flights including options for search, booking, payment and confirmation
#         - Diagram Type: Use Case Diagram
#         - PlantUML:
#             @startuml
#             left to right direction
#             actor User
#             rectangle FlightBooking {{
#                 User -- (Search Flights)
#                 User -- (Book Flight)
#                 User -- (Make Payment)
#                 User -- (Get Confirmation)
#                 (Search Flights) -- (Book Flight) : includes
#                 (Book Flight) -- (Make Payment) : includes
#                 (Make Payment) -- (Get Confirmation) : includes
#             }}
#             @enduml
#         - Insights: This describes the core functionalities of a flight booking system available to a user.
#         - Diagram Description: This diagram represents the different actions a user performs when booking a flight.

#         - Input: A class with properties like name, author, pages and methods for read and write.
#         - Diagram Type: Class Diagram
#         - PlantUML:
#             @startuml
#             class Book {{
#                 -String name
#                 -String author
#                 -int pages
#                 +read()
#                 +write()
#             }}
#             @enduml
#         - Insights: This represents the data structure for a book with its attributes and methods.
#         - Diagram Description: This is the class diagram of a book class showing its attributes and methods.

#         - Input: Instances of a student class object with the attributes of name and registration number
#         - Diagram Type: Object Diagram
#         - PlantUML:
#             @startuml
#             object Student1 {{
#                 name = "John Doe"
#                 reg_number = 12345
#             }}
#             object Student2 {{
#                 name = "Jane Smith"
#                 reg_number = 67890
#             }}
#             @enduml
#         - Insights: This diagram presents instances of the `Student` class with example data.
#         - Diagram Description: This is the object diagram that shows examples of student objects and their attributes.

#         - Input: A system process where a customer order is received, then validated, sent to fulfilment, and the customer gets a notification
#         - Diagram Type: Activity Diagram
#         - PlantUML:
#             @startuml
#             (*) --> "Receive Order"
#             --> "Validate Order"
#             --> "Send to Fulfilment"
#             --> "Notify Customer"
#             --> (*)
#             @enduml
#         - Insights: This demonstrates the process flow for how customer orders are managed by the system.
#         - Diagram Description: This is the activity diagram that illustrates the sequence of activities in processing a customer order.

#         - Input: A system process where a web application uses the frontend and the backend, as well as the database
#         - Diagram Type: Component Diagram
#         - PlantUML:
#             @startuml
#             [Frontend]
#             [Backend]
#             [Database]
#             [Frontend] --> [Backend]
#             [Backend] --> [Database]
#             @enduml
#         - Insights: This represents the standard structure of a web application with a clear separation between frontend, backend, and database.
#         - Diagram Description: This diagram shows the different components of the web application and their relation.

#         - Input: A deployment diagram with a web server, application server and a database
#         - Diagram Type: Deployment Diagram
#         - PlantUML:
#             @startuml
#             node "Web Server" as web {{
#                 component "Web Application"
#             }}
#             node "Application Server" as app {{
#                 component "Application Logic"
#             }}
#             database "Database Server" as db {{
#                 database "Data Storage"
#             }}
#             web -- app
#             app -- db
#             @enduml
#          - Insights: This represents the deployment of a typical web application with dedicated servers for web, application logic, and data.
#          - Diagram Description: This diagram illustrates how the different servers are deployed for a web application.

#         - Input: A door opening using a key and transitioning to the door opened state
#         - Diagram Type: State Diagram
#         - PlantUML:
#             @startuml
#             state Closed
#             state Opened
#             Closed --> Opened : key inserted
#             Opened --> Closed : key removed
#             @enduml
#         - Insights: This represents a simple state machine for a door with two distinct states based on a key insertion/removal.
#         - Diagram Description: This is the state diagram for a door that illustrates how the door changes states depending on the key.

#         - Input: A process where a user starts an action, the system responds, and then an event occurs to finish the action.
#         - Diagram Type: Timing Diagram
#         - PlantUML:
#             @startuml
            
            
#             |User |
#             |#LightBlue|System|
            
#             [->User: Start Action
#             User -> System: Action Request
#             activate System
#             System -->> User: Response
#             deactivate System
#             [-->System: Event Occurs
#             @enduml
#         - Insights: This represents the timing of various events in a user-system interaction including a system response and a final event.
#         - Diagram Description: This diagram displays the time and order of user-system interaction steps.


#     Based on the input, generate the PlantUML code, insights, and diagram description in a structured manner.
#     Input: {text_description}
#     PlantUML:
#     """
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
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

#     # Step 1: Generate PlantUML code
#     plantuml_code, text_response, diagram_description = generate_plantuml_gemini(request.description, request.model)

#     if plantuml_code.startswith("Error"):
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)

#     return {
#         "uml_text": plantuml_code,
#         "text_response": text_response,
#         "diagram_description": diagram_description
#     }










# Best of Both Worlds



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

class FlowchartRequest(BaseModel):
    description: str
    model: str = "gemini-pro"

class ModifyUMLRequest(BaseModel):
    uml_code: str
    diagram_instruction: str
    model: str = "gemini-pro"

def generate_plantuml_gemini(text_description, model_name, diagram_type="UML"):
    """
    Converts a text description to PlantUML code using the Gemini API synchronously.

    Args:
        text_description: A string describing the system or relationship.
        model_name: The name of the Gemini model to use.
        diagram_type: Type of diagram, either 'UML' or 'flowchart'

    Returns:
        A string containing the PlantUML code or an error message.
    """
    try:
        model = genai.GenerativeModel(model_name)

        if diagram_type == "UML":
            prompt = f"""
        You are an expert in generating PlantUML diagrams from textual descriptions. Your task is to create accurate PlantUML code that precisely represents the system described. Alongside the code, provide a clear explanation of the system, detailing its components, their interactions, and overall functionality. Additionally, include a concise summary of what the diagram depicts and its purpose. To enhance understanding, highlight the key elements and relationships within the diagram, ensuring clarity and relevance to the given description.

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
        elif diagram_type == "flowchart":
            prompt = f"""
            You are an expert in creating PlantUML flowcharts from text descriptions. Your goal is to convert the textual input into a syntactically correct PlantUML flowchart code. The generated flowchart should accurately represent the processes or steps described. Along with the PlantUML code, also provide a brief summary of the system's process and the diagram's purpose.

            Here are some examples of textual descriptions and their corresponding flowcharts. Adhere to these examples in your response:

            Example 1:
            - Input: A user opens the application, which then loads the main menu. The user selects an option, which loads the corresponding section. After they have finished with the selection the main menu is loaded again.
            - PlantUML:
                @startuml
                (*) --> "Open Application"
                --> "Load Main Menu"
                --> "Select Option"
                --> "Load Section"
                --> "Load Main Menu"
                --> (*)
                @enduml
            - Insights: This represents the basic flow for how the user interacts with an application.
            - Diagram Description: This diagram shows the flow from application open, user interaction and finally returning to the main menu

            Example 2:
            - Input: An order is received from a customer, it is then validated, then sent to fulfilment after which they get a notification
            - PlantUML:
                @startuml
                (*) --> "Receive Order"
                --> "Validate Order"
                --> "Send to Fulfilment"
                --> "Notify Customer"
                --> (*)
                @enduml
            - Insights: This diagram shows the core steps involved in processing a customer order.
            - Diagram Description: This flowchart outlines the different steps of order processing and notification.

            Example 3:
            - Input: A user provides a login request to a system, if the username and password are valid, they are redirected to the main page, otherwise a failure message is provided.
             - PlantUML:
                @startuml
                (*) --> "Login Request"
                --> "Validate Login"
                if "Success" then
                    -->[Yes] "Main Page"
                else
                    -->[No] "Failure Message"
                endif
                --> (*)
                @enduml
              - Insights: This diagram illustrates the conditional logic based on the login request.
            - Diagram Description: This flowchart shows how a system responds to valid and invalid login requests

            Based on the input, generate the PlantUML code and the insights about the diagram.
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

def modify_plantuml_gemini(uml_code, diagram_instruction, model_name):
    """
    Modifies the PlantUML code based on textual instructions using the Gemini API.
    """
    try:
        model = genai.GenerativeModel(model_name)

        prompt = f"""
        You are an expert in modifying PlantUML diagrams based on textual instructions. Given the current PlantUML code and a new instruction, your task is to modify the existing PlantUML code accordingly. Ensure the output is a syntactically correct and complete PlantUML code without any additional text or comments. Your modifications should precisely follow the user’s instructions while adhering to correct PlantUML syntax.
        
        Here are some examples of modification instructions. Please ensure the output is the code itself, without any additional text. 
        
        Example 1:
        Current PlantUML Code:
        @startuml
        [User]
        [WebApplication]
        [Database]
        User --> WebApplication
        WebApplication --> Database
        @enduml
        
        Instruction: Add a load balancer between the web application and the user.
        
        Modified PlantUML code:
        @startuml
        [User]
        [LoadBalancer]
        [WebApplication]
        [Database]
        User --> LoadBalancer
        LoadBalancer --> WebApplication
        WebApplication --> Database
        @enduml
        
        Example 2:
        Current PlantUML Code:
        @startuml
        actor User
        participant System
        User -> System: Login Request (username, password)
        activate System
        System -> System: Validate Credentials
        System --> User: User Details
        deactivate System
        @enduml
        
        Instruction: Change the user to an 'Admin' user and add another user called 'Guest'.
        
        Modified PlantUML code:
        @startuml
        actor Admin
        actor Guest
        participant System
        Admin -> System: Login Request (username, password)
        activate System
        System -> System: Validate Credentials
        System --> Admin: User Details
        deactivate System
        @enduml
        
        Example 3:
        Current PlantUML Code:
        @startuml
        class Book {{
            -String name
            -String author
            -int pages
            +read()
            +write()
        }}
        @enduml
        
        Instruction: Add a new attribute for year and a method for updating the book.
        
        Modified PlantUML code:
        @startuml
        class Book {{
            -String name
            -String author
            -int pages
            -int year
            +read()
            +write()
            +update()
        }}
        @enduml
        
        Current PlantUML Code:
        {uml_code}
        
        Instruction: {diagram_instruction}
        Modified PlantUML Code:
        """
        start_time = time.time()
        response = model.generate_content(prompt)
        end_time = time.time()
        print(f"Time taken to modify: {end_time - start_time}")
        if response.text:
            match = re.search(r'@startuml.*?@enduml', response.text, re.DOTALL)
            if match:
                 return match.group(0).strip()
            else:
                return "Could not find modified PlantUML code in the output from Gemini API."
        else:
            return "Gemini API returned an empty response."
    except Exception as e:
        return f"Error during processing: {e}"


@app.post('/generate_uml')
async def generate_uml(request: UMLRequest):
    if not request.description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

    # Step 1: Generate PlantUML code
    plantuml_code, text_response, diagram_description = generate_plantuml_gemini(request.description, request.model, "UML")

    if plantuml_code.startswith("Error"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)

    return {
        "uml_text": plantuml_code,
        "text_response": text_response,
        "diagram_description": diagram_description
    }

@app.post('/generate_flowchart')
async def generate_flowchart(request: FlowchartRequest):
    if not request.description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

    # Step 1: Generate PlantUML code
    plantuml_code, text_response, diagram_description = generate_plantuml_gemini(request.description, request.model, "flowchart")

    if plantuml_code.startswith("Error"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)

    return {
        "uml_text": plantuml_code,
        "text_response": text_response,
        "diagram_description": diagram_description
    }


@app.post('/modify_uml')
async def modify_uml(request: ModifyUMLRequest):
    if not request.uml_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide the current UML code.")
    if not request.diagram_instruction:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide the diagram instruction to modify.")

    modified_uml_code = modify_plantuml_gemini(request.uml_code, request.diagram_instruction, request.model)

    if modified_uml_code.startswith("Error"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=modified_uml_code)

    return {
        "uml_text": modified_uml_code
    }