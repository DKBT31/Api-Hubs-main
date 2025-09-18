import requests
import json

def test_upload_endpoint():
    """Test the /upload endpoint with a simple text file"""
    url = "http://localhost:9000/upload"
    
    # Create a simple test file
    test_content = """
    John Doe
    Software Engineer
    Email: john.doe@example.com
    Phone: +1-234-567-8900
    Address: 123 Main St, City, State
    
    Experience:
    - 5 years in Python development
    - FastAPI and web services
    - Machine Learning projects
    
    Education:
    - Bachelor's in Computer Science
    - Master's in Software Engineering
    """
    
    # Save test content to a file
    with open("test_document.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        # Test the upload endpoint
        with open("test_document.txt", "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            response = requests.post(url, files=files)
        
        print("Status Code:", response.status_code)
        print("Response Headers:", dict(response.headers))
        print("Response Content:")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except:
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the server is running on http://localhost:9000")
    except Exception as e:
        print(f"Error: {e}")

def test_server_health():
    """Test if the server is responding"""
    try:
        response = requests.get("http://localhost:9000/docs")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            print("📖 API Documentation available at: http://localhost:9000/docs")
        else:
            print(f"⚠️  Server responded with status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not accessible. Make sure it's running on port 9000")
    except Exception as e:
        print(f"❌ Error checking server: {e}")

if __name__ == "__main__":
    print("=== Testing API Server ===")
    
    print("\n1. Testing server health...")
    test_server_health()
    
    print("\n2. Testing upload endpoint...")
    test_upload_endpoint()
    
    print("\n=== Test Complete ===")
