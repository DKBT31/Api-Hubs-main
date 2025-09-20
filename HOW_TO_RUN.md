# 🚀 ResumeAI Parser - How to Run

## 📋 **Quick Start (3 Steps)**

### **1. Navigate to Project**
```powershell
cd "C:\Users\thuan\Downloads\Api-Hubs-main\Api-Hubs-main"
```

### **2. Install Dependencies (First time only)**
```powershell
pip install -r requirements.txt
```

### **3. Run the Application**
```powershell
.\start_venv.ps1
```

**That's it!** 🎉

---

## 🎯 **What You'll See**

```
🚀 ResumeAI Parser - Starting in Virtual Environment
✅ Tesseract found and added to PATH
📦 Activating virtual environment...
🚀 Starting ResumeAI Parser...
📱 API Documentation: http://127.0.0.1:9003/docs

✅ Tesseract OCR initialized successfully
✅ EasyOCR initialized successfully
✅ Gemini AI configured successfully!
🔍 OCR Capabilities:
   Tesseract: ✅ Available
   EasyOCR: ✅ Available
   Total engines: 2
INFO: Uvicorn running on http://127.0.0.1:9003
```

---

## 🔧 **Alternative Methods**

### **Manual Virtual Environment**
```powershell
# Activate venv
.venv\Scripts\Activate.ps1

# Add Tesseract (optional, for dual OCR)
$env:PATH += ";C:\Program Files\Tesseract-OCR"

# Run server
python main.py
```

### **One-liner**
```powershell
.venv\Scripts\python.exe main.py
```

---

## 📱 **Using the API**

### **Option 1: Web Interface (Easiest)**
1. Go to: **http://127.0.0.1:9003/docs**
2. Click "POST /upload"
3. Click "Try it out"
4. Upload your resume file
5. Click "Execute"

### **Option 2: Command Line**
```bash
curl -X POST "http://127.0.0.1:9003/upload" -F "file=@your_resume.pdf"
```

---

## � **Stop the Server**
Press `Ctrl+C` in the terminal

---

## ⚡ **Performance**
- **Text PDFs**: < 1 second
- **Image PDFs**: 2-5 seconds per page  
- **Accuracy**: 85-95% depending on quality
- **Supported**: PDF, DOC, DOCX, PNG, JPG
- **Languages**: English, Vietnamese

---

## 🔍 **OCR Engines**
- ✅ **EasyOCR**: Always available (AI-powered)
- ✅ **Tesseract**: Auto-detected if installed
- 🎯 **Both engines**: Maximum accuracy and speed

Your ResumeAI Parser is ready! 🎉
* Starting web service...
INFO:     Started server process [XXXX]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9002 (Press CTRL+C to quit)
```

### **Step 7: Test the API**
Open your browser and go to:
- **API Documentation**: http://127.0.0.1:9002/docs
- **Upload Endpoint**: http://127.0.0.1:9002/upload

---

## 🛠️ **Detailed Setup Instructions**

### **For Windows Users:**

1. **Open PowerShell as Administrator**
   ```powershell
   # Navigate to project directory
   cd "c:\Users\thuan\Downloads\Api-Hubs-main\Api-Hubs-main"
   
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   .venv\Scripts\activate.bat
   # or
   .venv\Scripts\Activate.ps1
   
   # Install packages
   pip install -r requirements.txt
   
   # Run the server
   python main.py
   ```

2. **If you get execution policy error:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **1. Port Already in Use**
```
ERROR: [Errno 10048] error while attempting to bind on address
```
**Solution:** Change port in `main.py`:
```python
uvicorn.run(app, host="127.0.0.1", port=9003)  # Change port number
```

#### **2. Missing API Key**
```
Warning: GEMINI_API_KEY not found
```
**Solution:** Create `.env` file with your API key:
```
GEMINI_API_KEY=your_api_key_here
```

#### **3. Package Installation Errors**
```bash
# Update pip first
python -m pip install --upgrade pip

# Install packages one by one if needed
pip install fastapi uvicorn pyyaml python-multipart tika
pip install pdfminer numpy pdf2image opencv-python pdfplumber
pip install google-generativeai python-dotenv requests
```

#### **4. PDF Processing Issues**
If you get PDF processing errors, install poppler:
- **Windows**: Download from https://poppler.freedesktop.org/
- **macOS**: `brew install poppler`
- **Ubuntu**: `sudo apt-get install poppler-utils`

---

## 📱 **How to Use the API**

### **Method 1: Using Swagger UI (Recommended)**
1. Go to http://127.0.0.1:9002/docs
2. Click on "POST /upload"
3. Click "Try it out"
4. Choose a PDF, DOC, or DOCX file
5. Click "Execute"
6. View the extracted JSON response

### **Method 2: Using curl**
```bash
curl -X POST "http://127.0.0.1:9002/upload" \
     -F "file=@path/to/your/resume.pdf"
```

### **Method 3: Using Python requests**
```python
import requests

url = "http://127.0.0.1:9002/upload"
files = {'file': open('resume.pdf', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### **Method 4: Using Postman**
1. Create new POST request
2. URL: `http://127.0.0.1:9002/upload`
3. Body → form-data
4. Key: `file` (type: File)
5. Value: Select your resume file
6. Send request

---

## 📊 **Expected Response Format**

```json
{
  "status": "success",
  "gemini_response": {
    "fullname": "CANDIDATE NAME",
    "phone": "PHONE NUMBER", 
    "profession": "JOB TITLE",
    "specialty": "SPECIALIZATIONS",
    "skill": ["skill1", "skill2", "skill3"],
    "education": [
      {
        "name": "SCHOOL NAME",
        "location": "CITY, COUNTRY",
        "period": "START - END"
      }
    ],
    "context": "PROFESSIONAL SUMMARY"
  },
  "extracted_text_length": 1576
}
```

---

## 🚦 **Server Status Indicators**

### **✅ Success:**
```
✅ Gemini API configured successfully!
INFO: Uvicorn running on http://127.0.0.1:9002
```

### **⚠️ Warnings:**
```
Warning: GEMINI_API_KEY not found. Gemini features will be disabled.
```

### **❌ Errors:**
```
ERROR: [Errno 10048] error while attempting to bind on address
```

---

## 🛑 **Stopping the Server**

Press `Ctrl+C` in the terminal where the server is running:
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
```

---

## 🔄 **Development Mode**

For development with auto-reload:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 9002
```

---

## 📋 **Project Structure**
```
ResumeAI-Parser/
├── main.py              # FastAPI server
├── requirements.txt     # Dependencies
├── .env                # API keys (create this)
├── configs/
│   └── config.yaml     # Configuration
├── utils/
│   ├── clear_text.py   # Text cleaning
│   ├── extract_text.py # Document extraction
│   ├── gemini_service.py # AI processing
│   └── util.py         # Utilities
└── README.md           # Documentation
```

---

That's it! Your ResumeAI Parser should now be running and ready to process resumes! 🎉