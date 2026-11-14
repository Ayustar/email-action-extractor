from google import genai

client = genai.Client()

for chunk in client.models.generate_content_stream(
    model="gemini-3.5-flash-lite",
    contents="Explain what an API is in about 100 words.",
):
    print(chunk.text, end="", flush=True)

print()
