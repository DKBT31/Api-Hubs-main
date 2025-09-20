import google.generativeai as gemini
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Cấu hình GenAI với API Key trực tiếp
api_key = os.getenv("GEMINI_API_KEY", "")  # API Key từ environment variable
if api_key:
    gemini.configure(api_key=api_key)
    # Khởi tạo mô hình Gemini
    model = gemini.GenerativeModel('gemini-1.5-flash')
    print("✅ Gemini API configured successfully!")
else:
    model = None
    print("Warning: GEMINI_API_KEY not found. Gemini features will be disabled.")

features = '''
context, Abbreviation, profession, specialty
'''

'''
fullname, phone, skill, học vấn
'''
def extract_feature_text(texts:str):
    if not model:
        # Return a fallback response when Gemini is not available
        return {
            "error": "Gemini API not configured",
            "message": "Please set GEMINI_API_KEY environment variable",
            "extracted_text": texts[:500] + "..." if len(texts) > 500 else texts
        }
    
    try:
        all_text = texts
        # First, let the model read and understand the content
        response = model.generate_content(f"Read the content of {all_text} and store it no need to respond")
        
        # Then extract specific features
        question = f"I want to extract information from {all_text} and return the information: {features} format it as JSON with keys: context, abbreviation, profession, specialty, fullname, phone, skill, education"
        response1 = model.generate_content(question)
        # # Reccommend the CV content and suggest improvements
        # question = f"Based on the content of {all_text}, please suggest improvements to make the CV more appealing to recruiters."
        # response2 = model.generate_content(question)

        response = response1# + "\n\nSuggestions for improvement:\n" + response2
        
        if response.text:
            return {
                "status": "success",
                "gemini_response": response.text,
                "extracted_text_length": len(texts)
            }
        else:
            return {
                "error": "No response from Gemini",
                "extracted_text": texts[:500] + "..." if len(texts) > 500 else texts
            }
            
    except Exception as e:
        return {
            "error": "Gemini API error", 
            "message": str(e),
            "extracted_text": texts[:500] + "..." if len(texts) > 500 else texts
        }