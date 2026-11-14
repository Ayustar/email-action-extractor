from pydantic import BaseModel
from google import genai
from google.genai import types

client = genai.Client(
    http_options=types.HttpOptions(timeout=15000)
)


class EmailSummary(BaseModel):
    summary: str
    sender_ask: str | None
    deadline: str | None
    action_needed: bool


email = """
Hi team,

Just a heads-up that the office will be closed on Monday for the
public holiday. Enjoy the long weekend!

Best,
Amaka
"""

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=f"Summarise this email:\n{email}",
    config=types.GenerateContentConfig(
        temperature=0.0,
        response_mime_type="application/json",
        response_schema=EmailSummary,
    ),
)

print(response.text)
print(type(response.parsed))
print(response.parsed.deadline)