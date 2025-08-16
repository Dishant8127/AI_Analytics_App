# Import the Python SDK
import google.generativeai as genai

# from google.colab import userdata
api_key = "AIzaSyDhqOB3hbv4EpLPms2PWnte4Dx2z5_TCTQ"


genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content("Hello world")
print(response.text)