from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

print("KEY:", os.getenv("GEMINI_API_KEY")[:10], "...")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say only Hello"
)

print(response.text)