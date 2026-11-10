import google.generativeai as genai
from src.config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


def generate_response(question):
    response = model.generate_content(question)
    return response.text