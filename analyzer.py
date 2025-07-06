import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def analyze_logs(log_text):
    prompt = f"""
You are a DevOps assistant. Analyze the logs below and identify possible causes of high CPU usage.

Logs:
{log_text}
"""
    response = model.generate_content([prompt])
    return response.text
