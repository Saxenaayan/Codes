
# UMLCopilot

An AI chatbot that generates UML diagrams and code from text descriptions using PlantUML.


## Demo

View the latest demo here



## Features

- **Generative AI-Powered UML Creation :** Converts user descriptions into UML diagrams using PlantUML and AI models, generating both code and diagrams.

- **Interactive Chat Interface:** Users interact via a chat window, receiving real-time text responses and visual diagram suggestions.

- **Model Selection:** Choose from different AI models (e.g., Gemini-Pro) for tailored diagram generation.

- **Dual-Tab Layout:** One tab shows the generated UML diagram with a download option, while the other displays the editable PlantUML code.

- **Image Download:** Download UML diagrams as PNG images with automatic file extension and MIME type detection.

- **Real-Time Feedback:** Provides error handling and informative messages for issues like network errors or invalid input.

- **Sidebar Options:** Allows model selection and offers chatbot functionality description, along with previous chat history.

- **Persistent State:** Maintains session state for user inputs, UML code, and generated diagrams across interactions.

- **Customizable Code:** Users can edit and regenerate PlantUML code to adjust the diagram.

- **Secure & Error-Resilient:** Handles errors smoothly, ensuring a seamless experience even with network or input issues.

 

## Table of Contents

1. [Installation](#installation)
2. [How to Run](#how-to-run)
3. [Deployment](#deployment)
4. [Project Structure](#project-structure)
5. [Environment Variables](#environment-variables)
6. [Tech Stack](#tech-stack)
7. [Future Enhancements](#future-enhancements)
8. [License](#license)
9. [Acknowledgments](#acknowledgements)
10. [Contributions](#contributions)
11. [Contact](#contact)
12. [FAQ](#FAQ)




## 1. Installation

Install required libraries:

```bash
  pip install streamlit requests plantuml ipython uvicorn
```
    
## 2. How to Run

Start the Backend:

```bash
  uvicorn main:app
```

Start the Frontend (Streamlit):

```bash
  streamlit run app.py

```
Terminate the Backend:

```bash
  To stop the backend server, press CTRL+C in the terminal where Uvicorn is running.

```



## 3. Deployment

To deploy this project run

```bash
  npm run deploy
```



## 4. Project Structure


### Files and Directories:

- **app.py**
- **models/**
- **utils/**
- **requirements.txt** : 
     `pip install -r requirements.txt`.
- **README.md**
- **.streamlit/**

## 5. Environment Variables

### 1. `PLANTUML_URL` : 
**Description:** Specifies the URL of the PlantUML server used to generate diagrams from UML code. This can be the public server (http://www.plantuml.com/plantuml/img/) or a private/local server for better security or offline functionality.

**Default Value:** http://www.plantuml.com/plantuml/img/

**Usage:** Modify this if you hostPLANTUML_URL:

 your PlantUML server, e.g., http://localhost:8080/plantuml/img/.

**How to Set:** Include it in your .env file or export it in your shell: export PLANTUML_URL=<server_url>.



### 2. `API_URL`
**Description:** Defines the backend service endpoint for generating UML descriptions. The application sends user inputs to this endpoint to generate PlantUML code and diagrams.

**Default Value:** http://127.0.0.1:8000/generate_uml

**Usage:** Update this variable when deploying the application to production or using a different backend service.

**How to Set:** Set it in the environment or a configuration file: export API_URL=<backend_url>.
 
### 3. `MODEL_NAME`
**Description:** Determines the AI model to be used for processing UML descriptions. Supported models include gemini-pro, gemini-pro-vision, gemini-1.0-pro, and gemini-1.0-pro-001.

**Default Value:** gemini-pro

**Usage:** Change this variable to experiment with different AI models based on their features and performance.

**How to Set:** Use environment variables or a .env file: export MODEL_NAME=gemini-pro.

### Gemini Models Explained

**gemini-pro:** A robust general-purpose model for generating UML diagrams from text-based descriptions, offering a balance between accuracy and speed.

**gemini-pro-vision:** An advanced model with enhanced visualization capabilities, particularly useful for detailed and complex UML diagrams.

**gemini-1.0-pro:** A lightweight model optimized for basic UML diagram generation with minimal resource usage.

**gemini-1.0-pro-001:** An experimental version of gemini-1.0-pro designed for testing new features and optimizations.


## 6. Tech Stack


**Frontend:** Streamlit

**Backend:** Python

**AI Model:**  gemini-pro, gemini-pro-vision, gemini-1.0-pro, gemini-1.0-pro-001
 
**Deployment:** Streamlit Cloud


## 7. Future Enhancements 

- Support for multilingual conversations.
- Integration with external databases for storing chat histories.
- Integrating Login/Sign-up Google Authentication 
- Implementing custom themes for the UI.
## 8. License

This project is licensed under the MIT License. See the LICENSE file for details.
## 9. Acknowledgements

**Gemini Models**

- gemini-pro: Designed for optimized performance in general UML tasks.
- gemini-pro-vision: Incorporates enhanced visualization and pattern recognition.
- gemini-1.0-pro: A reliable version for standard UML diagram elements.
- gemini-1.0-pro-001: The latest iteration with superior context understanding for complex requirements.
**Technologies**

- Python for backend functionality.
- Streamlit for the user interface.
- PlantUML for generating UML diagrams.
- Requests library for seamless API interactions.


## 10. Contributions

This project was developed by:

- Ayan Saxena

- Piyush Gupta

- Krrishna Gulati

- Ritwik Bhandari

- Ananya Baghel

Under the mentorship of **Sunny Anand**.

Feel free to submit issues or pull requests for improvements and bug fixes. Contributions are always welcome!
## 11. Contact

For any queries or support, feel free to contact:

Name: Ayan Saxena

Email: saxenaayan2@gmail.com

LinkedIn: https://www.linkedin.com/in/ayan-saxena-5b8946341?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app
## 12. FAQ

#### How do I interact with the chatbot?

Type your UML diagram description in the input box, and the chatbot will generate a diagram and its PlantUML code.

#### What formats are supported for diagram downloads?

The generated UML diagrams can be downloaded as PNG files.

#### Can I use my own PlantUML server?
Yes, you can configure the application to use your private PlantUML server by setting the PLANTUML_URL.

#### Can I add more AI models?
Yes, you can add models to the model_name dropdown in the sidebar and configure them in the backend.

