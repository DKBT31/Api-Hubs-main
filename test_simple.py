import requests
import json

def test_with_simple_text():
    """Test the API with a simple text file"""
    url = "http://127.0.0.1:9001/upload"
    
    # Create a simple test text file
    test_content = """
    NGUYEN VAN ANH
    Software Engineer
    
    Contact Information:
    Email: nguyen.van.anh@gmail.com
    Phone: +84-123-456-789
    
    Experience:
    - 3 years Python development
    - FastAPI and web services
    - Database design and optimization
    
    Skills:
    Python, JavaScript, SQL, Docker
    
    Education:
    Bachelor in Computer Science
    Ho Chi Minh City University of Technology
    """
    
    # Save to a temporary text file
    with open("test_resume.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        print("🚀 Testing API with simple text file...")
        
        with open("test_resume.txt", "rb") as f:
            files = {"file": ("test_resume.txt", f, "text/plain")}
            response = requests.post(url, files=files, timeout=30)
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("📋 Response from API:")
            try:
                result = response.json()
                print(json.dumps(result, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Raw response (not JSON):")
                print(response.text)
        else:
            print(f"❌ Error Response:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("=== Simple Text File Test ===")
    test_with_simple_text()
    print("=== Test Complete ===")
