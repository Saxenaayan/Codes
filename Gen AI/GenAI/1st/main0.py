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

        prompt = f"""You are an expert in generating PlantUML code from a text description.
        Your goal is to generate only the PlantUML code. Do not include any comments or explanations.
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
          
        Based on that, generate the PlantUML for this input:
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
                return plantuml_code
            else:
                return "Could not find PlantUML code in the output from Gemini API."
        else:
            return "Gemini API returned an empty response."

    except Exception as e:
        return f"Error during processing: {e}"


@app.post('/generate_uml')
async def generate_uml(request: UMLRequest):

    if not request.description:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a text description.")

    # Step 1: Generate PlantUML code
    plantuml_code = generate_plantuml_gemini(request.description, request.model)

    if plantuml_code.startswith("Error"):
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=plantuml_code)

    return {
        "uml_text": plantuml_code
    }