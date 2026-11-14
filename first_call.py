from google import genai
from google.genai import types

client = genai.Client()

for i in range(3):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Suggest a name for a small coffee shop. Reply with the name only.",
        config=types.GenerateContentConfig(temperature=1.0),
    )
    print(response.text)