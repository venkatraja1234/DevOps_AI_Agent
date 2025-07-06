import google.generativeai as genai

# Replace with your Gemini API key
genai.configure(api_key="AIzaSyCajPD9uYRvQA4Q_oJX6hqKbu5OJK1cJ2g")

# List all models available to your API key
models = genai.list_models()

print("✅ Available Gemini Models:")
for model in models:
    print(f"- {model.name}")
