import httpx
from google import genai
from google.genai import types, errors

client = genai.Client(
    http_options=types.HttpOptions(timeout=15000)
)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="In one sentence, what is an API?",
    )
    print(response.text)
except errors.APIError as e:
    print("Google answered with an error:", e.code, e.message)
except httpx.TransportError as e:
    print("Could not reach Google:", type(e).__name__)