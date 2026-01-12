import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: No API key found in environment.")
else:
    print(f"Testing key: {api_key[:10]}...")
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say hello")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")
