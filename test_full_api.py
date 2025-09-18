import requests
import json
import io

def test_upload_with_ai():
    """Test the /upload endpoint with AI processing enabled"""
    url = "http://127.0.0.1:9001/upload"
    
    # Create a comprehensive test document with resume-like content
    test_content = """
    NGUYỄN VĂN ANH
    Software Engineer | Full-Stack Developer
    
    THÔNG TIN LIÊN HỆ:
    Email: nguyen.van.anh@email.com
    Điện thoại: +84-123-456-789
    Địa chỉ: 123 Đường ABC, Quận 1, TP.HCM
    LinkedIn: linkedin.com/in/nguyenvananh
    
    TÓM TẮT:
    Kỹ sư phần mềm có 5 năm kinh nghiệm trong phát triển ứng dụng web và mobile.
    Chuyên về Python, JavaScript, và các framework hiện đại.
    
    KINH NGHIỆM LÀM VIỆC:
    
    Senior Software Engineer | Tech Company ABC (2022 - Hiện tại)
    - Phát triển và bảo trì hệ thống backend sử dụng Python/Django
    - Thiết kế API RESTful và microservices
    - Làm việc với Docker, Kubernetes, AWS
    - Quản lý team 3 developers junior
    
    Software Developer | StartUp XYZ (2020 - 2022)
    - Phát triển ứng dụng web với React.js và Node.js
    - Tích hợp payment gateway và third-party APIs
    - Optimization database performance (PostgreSQL, MongoDB)
    
    KỸ NĂNG:
    
    Ngôn ngữ lập trình: Python, JavaScript, TypeScript, Java
    Framework: Django, FastAPI, React.js, Vue.js, Express.js
    Database: PostgreSQL, MongoDB, Redis, MySQL
    Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD
    Tools: Git, Jira, Figma, Postman
    
    HỌC VẤN:
    
    Cử nhân Khoa học Máy tính | Đại học Bách Khoa TP.HCM (2016 - 2020)
    - GPA: 8.5/10
    - Đồ án tốt nghiệp: Hệ thống quản lý học tập online
    
    CHỨNG CHỈ:
    - AWS Certified Solutions Architect
    - Certified Kubernetes Administrator (CKA)
    - Google Cloud Professional Developer
    
    DỰ ÁN NỔI BẬT:
    
    E-commerce Platform (2023)
    - Xây dựng platform thương mại điện tử cho 10,000+ users
    - Sử dụng microservices architecture
    - Payment integration với VNPay, MoMo
    
    AI Chatbot System (2022)
    - Phát triển chatbot sử dụng NLP và machine learning
    - Tích hợp với Telegram, Facebook Messenger
    - Xử lý 1000+ conversations/day
    """
    
    try:
        # Create a file-like object in memory
        file_content = test_content.encode('utf-8')
        files = {
            'file': ('resume_test.txt', io.BytesIO(file_content), 'text/plain')
        }
        
        print("🚀 Testing API with AI processing...")
        print("📤 Uploading test resume...")
        
        response = requests.post(url, files=files, timeout=30)
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("📋 API Response:")
            try:
                result = response.json()
                print(json.dumps(result, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Raw response:")
                print(response.text)
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - AI processing may take some time")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on http://127.0.0.1:9001")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_server_status():
    """Check if the server is responding"""
    try:
        response = requests.get("http://127.0.0.1:9001/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            print("📖 API Documentation: http://127.0.0.1:9001/docs")
            return True
        else:
            print(f"⚠️  Server responded with status: {response.status_code}")
            return False
    except:
        print("❌ Server is not accessible")
        return False

if __name__ == "__main__":
    print("=== API-Hubs Full Functionality Test ===")
    print("Testing with Gemini AI enabled\n")
    
    print("1. Checking server status...")
    if check_server_status():
        print("\n2. Testing document upload and AI processing...")
        test_upload_with_ai()
    else:
        print("Server is not running. Please start the server first.")
    
    print("\n=== Test Complete ===")
    print("\n💡 Tips:")
    print("- The AI processing may take 10-30 seconds")
    print("- Try uploading PDF, DOC, or DOCX files for better results")
    print("- Check the API docs at http://127.0.0.1:9001/docs for interactive testing")
