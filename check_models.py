import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyCajPD9uYRvQA4Q_oJX6hqKbu5OJK1cJ2g")

# List available models
models = genai.list_models()

print("✅ Supported Gemini Models and Methods:")
for model in models:
    print(f"🔹 {model.name} — supports: {model.supported_generation_methods}")
