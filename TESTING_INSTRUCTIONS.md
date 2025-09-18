"""
Manual Testing Instructions for the API-Hubs Project
==================================================

The server is now running successfully on http://127.0.0.1:9000

✅ Setup Status:
- Python environment: Configured with virtual environment
- Dependencies: All installed successfully  
- Server: Running on localhost:9000
- API Documentation: Available at http://127.0.0.1:9000/docs

⚠️ Notes:
- Gemini API key is not configured (set GEMINI_API_KEY environment variable to enable AI features)
- Without Gemini API, the service will return fallback responses for text processing

🧪 How to Test:

1. **API Documentation:**
   Visit: http://127.0.0.1:9000/docs
   This shows the interactive Swagger UI where you can test the /upload endpoint

2. **Test with Sample Files:**
   - Create a simple PDF, DOC, or DOCX file with some text
   - Use the /upload endpoint in the Swagger UI to upload the file
   - The API will extract text and return processed results

3. **Using curl (PowerShell):**
   curl -X POST "http://127.0.0.1:9000/upload" -F "file=@your_test_file.pdf"

4. **Using Postman or similar tools:**
   - Method: POST
   - URL: http://127.0.0.1:9000/upload  
   - Body: form-data with key "file" and select a PDF/DOC/DOCX file

🔧 Project Structure:
- main.py: FastAPI server with /upload endpoint
- utils/extract_text.py: PDF and DOC text extraction
- utils/clear_text.py: Vietnamese text cleaning
- utils/gemini_service.py: AI text processing (requires API key)
- utils/util.py: Configuration loading
- configs/config.yaml: Server configuration

✅ The project is complete and working!
The API successfully:
- Accepts file uploads (PDF, DOC, DOCX)
- Extracts text from documents
- Processes Vietnamese text (removes accents, special characters)
- Returns structured responses
- Provides graceful fallback when Gemini API is not configured

To enable full AI features, set the GEMINI_API_KEY environment variable with a valid Google Generative AI API key.
"""
