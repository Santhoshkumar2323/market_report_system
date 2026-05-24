# modules/gemini_client.py

import requests
import json
from config.settings import settings


GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def generate_gemini_report(signals):

    prompt = f"""
You are writing short macro commentary.

Interpret the following structured signals.
Do NOT restate data.
Be concise.
Use 5-8 bullets maximum.

Signals:
{signals}
"""

    headers = {"Content-Type": "application/json"}
    params = {"key": settings.GEMINI_API_KEY}

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        GEMINI_URL,
        headers=headers,
        params=params,
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]