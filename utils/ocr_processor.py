"""
OCR Module for Image-based PDF Processing
Supports multiple OCR engines for consistent results
"""
import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import List, Tuple, Optional
from pdf2image import convert_from_path
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRProcessor:
    """
    Multi-engine OCR processor for extracting text from images and image-based PDFs
    """
    
    def __init__(self):
        self.tesseract_available = False
        self.easyocr_available = False
        self._initialize_ocr_engines()
    
    def _initialize_ocr_engines(self):
        """Initialize available OCR engines"""
        
        # Try to initialize Tesseract
        try:
            import pytesseract
            # Try to run tesseract to check if it's installed
            pytesseract.get_tesseract_version()
            self.tesseract_available = True
            logger.info("✅ Tesseract OCR initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Tesseract not available: {e}")
            logger.info("💡 Install Tesseract: https://github.com/tesseract-ocr/tesseract")
        
        # Try to initialize EasyOCR
        try:
            import easyocr
            self.easyocr_reader = easyocr.Reader(['en', 'vi'])  # English and Vietnamese
            self.easyocr_available = True
            logger.info("✅ EasyOCR initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ EasyOCR not available: {e}")
    
    def is_pdf_image_based(self, pdf_path: str, sample_pages: int = 2) -> bool:
        """
        Detect if a PDF is primarily image-based by checking text extractability
        """
        try:
            import pdfplumber
            
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_check = min(sample_pages, total_pages)
                
                text_found = 0
                for i in range(pages_to_check):
                    page = pdf.pages[i]
                    text = page.extract_text()
                    if text and len(text.strip()) > 50:  # Meaningful text threshold
                        text_found += 1
                
                # If less than 50% of sampled pages have meaningful text, consider it image-based
                is_image_based = (text_found / pages_to_check) < 0.5
                
                logger.info(f"PDF Analysis: {text_found}/{pages_to_check} pages have extractable text")
                logger.info(f"PDF Type: {'Image-based' if is_image_based else 'Text-based'}")
                
                return is_image_based
                
        except Exception as e:
            logger.warning(f"Could not analyze PDF type: {e}")
            return True  # Default to image-based processing
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply adaptive thresholding for better contrast
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Optional: Apply morphological operations to clean up
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text_tesseract(self, image: np.ndarray) -> str:
        """Extract text using Tesseract OCR"""
        if not self.tesseract_available:
            return ""
        
        try:
            import pytesseract
            
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Configure Tesseract for better accuracy
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵýỷỹ '
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=custom_config, lang='eng+vie')
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Tesseract OCR error: {e}")
            return ""
    
    def extract_text_easyocr(self, image: np.ndarray) -> str:
        """Extract text using EasyOCR"""
        if not self.easyocr_available:
            return ""
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Extract text with EasyOCR
            results = self.easyocr_reader.readtext(processed_image)
            
            # Combine all detected text
            text_parts = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # Filter low confidence results
                    text_parts.append(text)
            
            return ' '.join(text_parts)
            
        except Exception as e:
            logger.error(f"EasyOCR error: {e}")
            return ""
    
    def extract_text_from_image(self, image_input) -> str:
        """
        Extract text from image using multiple OCR engines for best results
        Accepts either numpy array or file path
        """
        # Handle different input types
        if isinstance(image_input, str):
            # It's a file path
            try:
                from PIL import Image
                pil_image = Image.open(image_input)
                image = np.array(pil_image)
            except Exception as e:
                logger.error(f"Failed to load image from path {image_input}: {e}")
                return ""
        elif isinstance(image_input, np.ndarray):
            # It's already a numpy array
            image = image_input
        else:
            logger.error(f"Unsupported image input type: {type(image_input)}")
            return ""
        
        texts = []
        
        # Try Tesseract
        if self.tesseract_available:
            tesseract_text = self.extract_text_tesseract(image)
            if tesseract_text:
                texts.append(("Tesseract", tesseract_text))
        
        # Try EasyOCR
        if self.easyocr_available:
            easyocr_text = self.extract_text_easyocr(image)
            if easyocr_text:
                texts.append(("EasyOCR", easyocr_text))
        
        if not texts:
            logger.warning("No OCR engines available or successful")
            return ""
        
        # For now, prefer EasyOCR if available, otherwise use Tesseract
        # In the future, we could implement text comparison and selection logic
        for engine, text in texts:
            if engine == "EasyOCR" and len(text) > 50:
                logger.info(f"Using EasyOCR result ({len(text)} chars)")
                return text
        
        # Fallback to longest result
        best_text = max(texts, key=lambda x: len(x[1]))
        logger.info(f"Using {best_text[0]} result ({len(best_text[1])} chars)")
        return best_text[1]
    
    def extract_text_from_multiple_images(self, image_paths: List[str]) -> str:
        """
        Extract text from multiple image files (e.g., multi-page CV as separate images)
        """
        all_text = []
        
        for i, image_path in enumerate(image_paths):
            logger.info(f"Processing image {i+1}/{len(image_paths)}: {os.path.basename(image_path)}")
            
            try:
                # Extract text from this image
                page_text = self.extract_text_from_image(image_path)
                
                if page_text:
                    all_text.append(f"--- Page {i+1} ({os.path.basename(image_path)}) ---")
                    all_text.append(page_text)
                    all_text.append("")
                else:
                    logger.warning(f"No text extracted from {os.path.basename(image_path)}")
                    
            except Exception as e:
                logger.error(f"Error processing {image_path}: {e}")
                all_text.append(f"--- Page {i+1} (Error) ---")
                all_text.append(f"Error processing image: {str(e)}")
                all_text.append("")
        
        combined_text = '\n'.join(all_text)
        logger.info(f"Multi-image OCR completed. Extracted {len(combined_text)} characters from {len(image_paths)} images")
        
        return combined_text

    def extract_text_from_pdf_images(self, pdf_path: str) -> str:
        """
        Extract text from image-based PDF using OCR
        """
        try:
            logger.info(f"Converting PDF to images: {pdf_path}")
            
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=300, fmt='JPEG')
            
            all_text = []
            
            for i, image in enumerate(images):
                logger.info(f"Processing page {i+1}/{len(images)}")
                
                # Convert PIL Image to numpy array
                img_array = np.array(image)
                
                # Extract text from this page
                page_text = self.extract_text_from_image(img_array)
                
                if page_text:
                    all_text.append(f"--- Page {i+1} ---")
                    all_text.append(page_text)
                    all_text.append("")
            
            combined_text = '\n'.join(all_text)
            logger.info(f"OCR completed. Extracted {len(combined_text)} characters")
            
            return combined_text
            
        except Exception as e:
            logger.error(f"Error processing PDF images: {e}")
            return f"Error extracting text from image PDF: {str(e)}"
    
    def get_ocr_status(self) -> dict:
        """Get status of available OCR engines"""
        return {
            "tesseract_available": self.tesseract_available,
            "easyocr_available": self.easyocr_available,
            "engines_count": sum([self.tesseract_available, self.easyocr_available])
        }

# Global OCR processor instance
ocr_processor = OCRProcessor()

def extract_text_with_ocr(pdf_path: str) -> Tuple[str, bool]:
    """
    Extract text from PDF with automatic OCR detection
    Returns: (extracted_text, used_ocr)
    """
    # Check if PDF is image-based
    is_image_based = ocr_processor.is_pdf_image_based(pdf_path)
    
    if is_image_based:
        logger.info("🔍 Image-based PDF detected, using OCR")
        text = ocr_processor.extract_text_from_pdf_images(pdf_path)
        return text, True
    else:
        logger.info("📄 Text-based PDF detected, using standard extraction")
        # Fall back to standard text extraction
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text_parts = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                return '\n'.join(text_parts), False
        except Exception as e:
            logger.warning(f"Standard extraction failed, trying OCR: {e}")
            text = ocr_processor.extract_text_from_pdf_images(pdf_path)
            return text, True