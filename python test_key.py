# test_key.py
import google.generativeai as genai

# --- IMPORTANT: Paste your key here ---
API_KEY = "AIzaSyDhqOB3hbv4EpLPms2PWnte4Dx2z5_TCTQ"

print("Attempting to connect to Google AI...")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("What is the capital of India?")
    
    print("\n✅ SUCCESS! Your API key is working.")
    print("AI Response:", response.text)

except Exception as e:
    print("\n❌ FAILED. There is a problem with your API key or connection.")
    print("Error Details:", e)