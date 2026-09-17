import os
import re
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Load API key from Streamlit Cloud Secrets or local .env
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it to Streamlit Secrets or .env."
    )

client = genai.Client(api_key=api_key)


# Model used for extraction
MODEL_NAME = "gemini-2.5-flash"


SYSTEM_PROMPT = """You are an assistant that extracts structured project information from raw,
unstructured project communication (chat logs, meeting notes, transcripts, emails).

Return ONLY valid JSON, no markdown fences, no preamble, matching this exact schema:

{
  "summary": "2-3 sentence summary of the conversation",
  "tasks": [
    {
      "task": "description of the action item",
      "owner": "name or role, or 'unassigned'",
      "deadline": "date/time mentioned, or 'none'"
    }
  ],
  "decisions": [
    "decision or approval that was made"
  ],
  "pending_approvals": [
    "open question or approval still awaited"
  ]
}

If a category has nothing relevant, return an empty array for it.
Do not invent information not present in the text.
"""


def generate_extraction(prompt: str) -> str:
    """Send a prompt to Gemini and return its text response."""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=1000,
            response_mime_type="application/json"
        )
    )

    return response.text


def extract_from_conversation(text: str) -> dict:
    """
    Call Gemini API to extract structured project information.
    Includes retry logic for JSON parsing errors.
    """

    user_prompt = f"""Extract structured project information from this conversation:

<<<CONVERSATION TEXT HERE>>>

{text}

<<<END CONVERSATION>>>
"""

    try:
        # First attempt
        response_text = generate_extraction(user_prompt)

        # Remove markdown fences if present
        response_text = re.sub(
            r"```json\n?|\n?```",
            "",
            response_text
        ).strip()

        # Parse JSON
        try:
            parsed = json.loads(response_text)
            return parsed

        except json.JSONDecodeError:

            # Retry with explicit JSON instructions
            retry_prompt = f"""Your previous response was not valid JSON.

Return ONLY valid JSON matching this schema:

{{
  "summary": "2-3 sentence summary",
  "tasks": [
    {{
      "task": "description",
      "owner": "name or unassigned",
      "deadline": "date or none"
    }}
  ],
  "decisions": [
    "decision text"
  ],
  "pending_approvals": [
    "approval text"
  ]
}}

Original conversation:

{text}
"""

            retry_text = generate_extraction(retry_prompt)

            retry_text = re.sub(
                r"```json\n?|\n?```",
                "",
                retry_text
            ).strip()

            parsed = json.loads(retry_text)
            return parsed

    except Exception as e:

        # Fallback error response
        return {
            "summary": "Error processing conversation",
            "tasks": [],
            "decisions": [],
            "pending_approvals": [
                f"Error: {str(e)}"
            ]
        }


def validate_extraction(extracted_data: dict) -> bool:
    """Validate that extraction has required fields."""

    required_fields = [
        "summary",
        "tasks",
        "decisions",
        "pending_approvals"
    ]

    return all(
        field in extracted_data
        for field in required_fields
    )