import time
import httpx
from google import genai
from google.genai import types, errors

client = genai.Client(
    http_options=types.HttpOptions(timeout=15000)
)


def call_model(prompt, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )
            return response.text
        except errors.ClientError as e:
            print("Your side (4xx), not retrying:", e.code, e.message)
            return None
        except (errors.ServerError, httpx.TransportError) as e:
            print(f"Attempt {attempt} failed: {type(e).__name__}")
            if attempt == max_attempts:
                print("Giving up.")
                return None
            wait = 2 ** attempt
            print(f"Waiting {wait}s, then retrying...")
            time.sleep(wait)


answer = call_model("In one sentence, what is an API?")
print(answer)