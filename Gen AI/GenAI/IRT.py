import google.generativeai as genai
from docx import Document
import json

def analyze_document(document_path, api_key):
    """
    Analyzes a Word document using the Gemini API to count words, letters, and lines.

    Args:
        document_path (str): The path to the Word document (.docx).
        api_key (str): Your Google Gemini API key.

    Returns:
       dict: A dictionary containing the word count, letter count, and line count, 
             or None if the document or API call fails.
    """
    try:
        # Extract text from the Word Document
        doc = Document(document_path)
        full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Prompt to the Gemini API to provide word count, line count and letter count

        prompt = f"""
        Please provide the count of words, letters and lines from below text.
        Text:
        {full_text}

        Response should be in the form of json:
        {{
           "word_count": "",
           "letter_count": "",
           "line_count":""
        }}
        """
        response = model.generate_content(prompt)

        if response.text:
           try:
              print(f"Raw Response from Gemini: {response.text}")  
              json_response = json.loads(response.text)
              return json_response
           except json.JSONDecodeError as e:
             print(f"Error decoding JSON: {e}")
             return None
        else:
          print("Error in API call, No Response Received")
          return None


    except FileNotFoundError:
        print(f"Error: Document not found at {document_path}")
        return None
    except Exception as e:
      print(f"An error occurred: {e}")
      return None

if __name__ == "__main__":

    document_path = r"C:\Users\saxen\Codes\Gen AI\GenAI\gamma chi square levy and brownian final 7 aug.docx"
    api_key = "AIzaSyBenqVyOUE6twWfJhQb0y4SxcHkwee-rt0"  

    analysis_results = analyze_document(document_path, api_key)

    if analysis_results:
      print(f"Document Analysis Results for: {document_path}")
      print(f"  Word Count: {analysis_results.get('word_count')}")
      print(f"  Letter Count: {analysis_results.get('letter_count')}")
      print(f"  Line Count: {analysis_results.get('line_count')}")
    else:
        print("Analysis failed. Please check the errors.")