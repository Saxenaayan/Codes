from flask import Flask, request, jsonify
import re
import google.generativeai as genai
import os
import time
import plantuml
from io import BytesIO
import base64
from PIL import Image

app = Flask(__name__)

# Set your Google API Key as an environment variable
GOOGLE_API_KEY = "AIzaSyBmiDw7yTizDpWpXtrj3vBV_hTnyj_juR4"


# Make sure your api key is initialized
if not GOOGLE_API_KEY:
    raise Exception("Error: Google API Key not found! Make sure that the environment variable GOOGLE_API_KEY is set!")

genai.configure(api_key=GOOGLE_API_KEY)


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


def generate_uml_diagram(plantuml_code, plantuml_path="plantuml"):
    """
    Generates a UML diagram image from PlantUML code.

    Args:
        plantuml_code: A string containing PlantUML code.
        plantuml_path: The path to your plantuml executable or jar.

    Returns:
        The encoded image as a string, or an error message.
    """
    try:
        if not os.path.exists(plantuml_path):
            raise Exception("PlantUML is not present at the specified location")
        diagram = plantuml.PlantUML(plantuml_path=plantuml_path)
        image_data = diagram.processes_bytes(plantuml_code, format="png")
        return base64.b64encode(image_data).decode('utf-8') # returns base64 representation of bytes
    except Exception as e:
        return f"Error during diagram generation: {e}"


@app.route('/generate_uml', methods=['POST'])
def generate_uml():
    data = request.get_json()
    description = data.get('description')
    model_name = data.get('model')


    if not description:
        return jsonify({"error": "Please provide a text description."}), 400

    # Step 1: Generate PlantUML code
    plantuml_code = generate_plantuml_gemini(description, model_name)

    if plantuml_code.startswith("Error"):
      return jsonify({"error": plantuml_code}), 500

    return jsonify({
        "uml_text": plantuml_code
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=8000)