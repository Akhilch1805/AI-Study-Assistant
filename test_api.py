import google.generativeai as genai
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAOjhOFmoYsDsPBDJIz2FkARlMJb43_w18")

def test_api():
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello, are you working?")
        print(f"API Key Test Successful: {response.text}")
    except Exception as e:
        print(f"API Key Test Failed: {e}")

if __name__ == "__main__":
    test_api()
