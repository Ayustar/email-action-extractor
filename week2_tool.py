import time
import httpx
from pydantic import BaseModel, Field
from google import genai
from google.genai import types, errors

client = genai.Client(
    http_options=types.HttpOptions(timeout=15000)
)


class ActionItem(BaseModel):
    task: str
    deadline: str | None
    condition: str | None = Field(
        description=(
            "List ALL requirements or circumstances that decide who the task "
            "applies to, such as eligibility rules about location, age or "
            "availability. NOT timing or politeness such as 'when you get a "
            "chance' or 'when you have it'. Use null if the task applies "
            "to everyone."
        )
    )


class EmailSummary(BaseModel):
    summary: str
    action_items: list[ActionItem]
    action_needed: bool


def summarise_email(email_text, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=f"Summarise this email:\n{email_text}",
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    system_instruction="The email is addressed to the user. In the summary, 'you' means the user who received it, and 'the sender' means the person who wrote it.",
                    response_mime_type="application/json",
                    response_schema=EmailSummary,
                ),
            )
            if response.parsed is None:
                print("Model's answer did not match the schema.")
                return None
            return response.parsed
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


if __name__ == "__main__":
    with open("email.txt", encoding="utf-8") as f:
        email = f.read()

    result = summarise_email(email)

    if result is None:
        print("No summary produced.")
    else:
        print("Summary:", result.summary)
        print("Action needed:", result.action_needed)
        for item in result.action_items:
            print("-", item.task, "| deadline:", item.deadline, "| condition:", item.condition)