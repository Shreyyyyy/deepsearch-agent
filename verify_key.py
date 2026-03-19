import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

print(f"Loaded API Key: {api_key[:10]}...")

try:
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello, are you there?"}],
        model="llama3-8b-8192"
    )
    print("API Response:", completion.choices[0].message.content)
except Exception as e:
    print("API Error:", e)
