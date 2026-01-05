import os
import openai
from dotenv import load_dotenv

load_dotenv()


class OpenAIConnector:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def complete(self, prompt: str, model: str = "gpt-4-turbo") -> dict:
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Tu fais partie du système Zéro Obstacle Canada."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=1500,
            )
            content = response.choices[0].message.content.strip()
            return {"status": "success", "result": content}
        except Exception as e:
            return {"status": "error", "error": str(e)}
from typing import Optional

from openai import OpenAI


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Return an OpenAI client using the provided or environment API key."""
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is not configured")

    return OpenAI(api_key=key)
