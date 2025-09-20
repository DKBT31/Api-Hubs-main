import uvicorn 
from fastapi import FastAPI, Form,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.util import load_config
from starlette.requests import Request
import time
import os
from utils.extract_text import pdf_extract, doc_extract
from utils.gemini_service import extract_feature_text

# Check OCR availability
try:
    from utils.ocr_processor import ocr_processor
    OCR_STATUS = ocr_processor.get_ocr_status()
except ImportError:
    OCR_STATUS = {"tesseract_available": False, "easyocr_available": False, "engines_count": 0}

origins = [
    "*"
]
app = FastAPI(
    title="ResumeAI Parser",
    description="Intelligent Document Processing & Resume Analysis API with OCR support",
    version="2.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ============= Define Config And Setting =============
CONFIG_PATH = "configs/config.yaml"
config = load_config(CONFIG_PATH)
# =====================================================

# Print OCR status on startup
print("🔍 OCR Capabilities:")
print(f"   Tesseract: {'✅ Available' if OCR_STATUS['tesseract_available'] else '❌ Not available'}")
print(f"   EasyOCR: {'✅ Available' if OCR_STATUS['easyocr_available'] else '❌ Not available'}")
print(f"   Total engines: {OCR_STATUS['engines_count']}")
if OCR_STATUS['engines_count'] == 0:
    print("⚠️  No OCR engines available. Run 'setup_ocr.ps1' to enable image PDF processing.")

# ============= Define Routes =============

@app.get("/")
async def root():
    return {
        "message": "ResumeAI Parser API",
        "version": "2.0.0",
        "features": ["PDF text extraction", "DOC/DOCX processing", "OCR for image PDFs", "AI-powered data extraction"],
        "ocr_status": OCR_STATUS
    }

@app.get("/ocr-status")
async def get_ocr_status():
    """Get OCR engine availability status"""
    return {
        "ocr_engines": OCR_STATUS,
        "supported_formats": {
            "text_pdfs": "✅ Always supported",
            "image_pdfs": "✅ Supported with OCR" if OCR_STATUS['engines_count'] > 0 else "❌ Requires OCR setup",
            "doc_docx": "✅ Always supported",
            "images": "✅ Supported with OCR" if OCR_STATUS['engines_count'] > 0 else "❌ Requires OCR setup"
        },
        "recommendations": [
            "Run setup_ocr.ps1 to install OCR engines" if OCR_STATUS['engines_count'] == 0 else "OCR ready for image processing",
            "EasyOCR recommended for complex layouts",
            "Tesseract recommended for speed"
        ]
    }

@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    '''
        Upload and process documents (PDF, DOC, DOCX) with AI extraction
        
        Supported formats:
        - PDF (text-based): Standard text extraction
        - PDF (image-based): OCR text extraction (requires OCR setup)
        - DOC/DOCX: Microsoft document processing
        - TXT: Plain text files
        
        Features:
        - Automatic detection of image vs text PDFs
        - Multi-engine OCR for better accuracy
        - Vietnamese text processing and cleaning
        - AI-powered structured data extraction
        
        Returns:
        - Structured JSON with extracted information
        - Processing metadata and statistics
    '''
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
    tmp_path = file.filename
    t0 = time.time()
    ImageBase64 = ''
    
    # Track processing method
    processing_method = "unknown"
    
    if ".pdf" in str(tmp_path):
        resume_text, ImageBase64 = pdf_extract(tmp_path)
        processing_method = "pdf_extraction"
    else:
        resume_text = doc_extract(tmp_path)
        processing_method = "document_extraction"
    
    resume_text = resume_text.replace("\t", " \t")
    processing_time = time.time() - t0
    
    print("data", extract_feature_text(resume_text))
    print("Processing time:", processing_time)
    
    # Safe file cleanup
    try:
        os.unlink(file.filename)
    except PermissionError:
        print(f"Warning: Could not delete temporary file {file.filename} - it may be in use")
    except Exception as e:
        print(f"Warning: Error deleting file {file.filename}: {e}")
    
    # Get AI extraction results
    ai_result = extract_feature_text(resume_text)
    
    # Enhanced response with metadata
    return {
        "success": True,
        "ai_extraction": ai_result,
        "metadata": {
            "filename": file.filename,
            "processing_method": processing_method,
            "processing_time_seconds": round(processing_time, 2),
            "text_length": len(resume_text),
            "ocr_available": OCR_STATUS['engines_count'] > 0,
            "file_type": "pdf" if ".pdf" in str(tmp_path) else "document"
        }
    }


if __name__ == "__main__":
	print("* Starting web service...")
	uvicorn.run(app, host="127.0.0.1", port=9003)