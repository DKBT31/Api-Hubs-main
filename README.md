# 📋 **ResumeAI Parser** 
*Intelligent Document Processing & Resume Analysis API*

## 🎯 **Project Overview**

**ResumeAI Parser** is a FastAPI-based intelligent document processing service that specializes in extracting structured information from resumes and CVs. It combines advanced text extraction techniques with Google's Gemini AI to automatically parse and organize resume data into structured JSON format.

## ✨ **Key Features**

- 🤖 **AI-Powered Extraction**: Uses Google Gemini 1.5 Flash for intelligent data parsing
- 📄 **Multi-Format Support**: PDF, DOC, DOCX, and TXT files
- 🇻🇳 **Vietnamese Language Support**: Specialized text cleaning and accent removal
- 🔧 **RESTful API**: FastAPI with automatic documentation
- 📊 **Structured Output**: Clean JSON format with standardized fields
- ⚡ **Fast Processing**: ~4 seconds average processing time
- 🛡️ **Error Handling**: Robust fallback mechanisms

## 🏗️ **Architecture**

```
ResumeAI Parser
├── FastAPI Server (main.py)
├── Document Processors
│   ├── PDF Extraction (pdfminer, pdfplumber, tika)
│   ├── DOC/DOCX Extraction (Apache Tika)
│   └── Text Cleaning (Vietnamese support)
├── AI Service (Google Gemini)
└── API Documentation (Swagger UI)
```

## 📋 **JSON Output Structure**

```json
{
  "status": "success",
  "gemini_response": {
    "fullname": "CANDIDATE NAME",
    "phone": "PHONE NUMBER",
    "profession": "JOB TITLE/FIELD",
    "specialty": "TECHNICAL SPECIALIZATIONS",
    "skill": ["skill1", "skill2", "skill3"],
    "education": [
      {
        "name": "INSTITUTION NAME",
        "location": "CITY, COUNTRY",
        "period": "START - END DATE"
      }
    ],
    "context": "PROFESSIONAL SUMMARY"
  },
  "extracted_text_length": 1576
}
```

## 🚀 **Getting Started**

### Prerequisites
- Python 3.8+
- Google Gemini API Key

### Installation
```bash
git clone <repository>
cd ResumeAI-Parser
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration
Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### Run Server
```bash
python main.py
```

Server will start at: `http://127.0.0.1:9002`
API Documentation: `http://127.0.0.1:9002/docs`

## 📚 **API Usage**

### Upload Resume
```bash
curl -X POST "http://127.0.0.1:9002/upload" \
     -F "file=@resume.pdf"
```

### Response Example
```json
{
  "status": "success",
  "gemini_response": "{ extracted data }",
  "extracted_text_length": 1576
}
```

## 🎯 **Use Cases**

1. **HR Automation**: Automatically parse incoming resumes
2. **Recruitment Platforms**: Extract candidate information for databases
3. **ATS Integration**: Feed structured data into applicant tracking systems
4. **Resume Analysis**: Analyze skill distributions and trends
5. **Data Migration**: Convert legacy resume formats to structured data

## 🛠️ **Technology Stack**

- **Backend**: FastAPI, Uvicorn
- **Document Processing**: Apache Tika, PDFMiner, PDFPlumber
- **AI Service**: Google Gemini 1.5 Flash
- **Text Processing**: Custom Vietnamese language utilities
- **API Documentation**: Swagger UI (auto-generated)

## 📈 **Performance**

- **Processing Speed**: 3-5 seconds per document
- **Supported Formats**: PDF, DOC, DOCX, TXT
- **Language Support**: Vietnamese + English
- **Accuracy**: High accuracy with AI-powered extraction
- **Scalability**: Async FastAPI architecture

## 🔒 **Security & Privacy**

- Files are processed temporarily and deleted after extraction
- No permanent storage of uploaded documents
- API key security through environment variables
- CORS support for secure frontend integration

## 📞 **Support**

For issues, feature requests, or contributions, please refer to the project documentation.

---

**ResumeAI Parser** - Making resume processing intelligent and effortless! 🚀
