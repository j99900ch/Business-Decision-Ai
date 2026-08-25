"""
=========================================================
Business DecisionAI
Google Gemini Integration
=========================================================
"""

from google import genai
from dotenv import load_dotenv
import os

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

# ---------------------------------------------------------
# Read API Key
# ---------------------------------------------------------

API_KEY = os.getenv("Business_Gemini_Key")

if not API_KEY:
    raise ValueError(
        "❌ GEMINI_API_KEY not found inside .env file."
    )

# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

client = genai.Client(
    api_key=API_KEY
)

# ---------------------------------------------------------
# Model Name
# ---------------------------------------------------------

MODEL_NAME = "gemini-2.5-flash"

# ---------------------------------------------------------
# Generate Response
# ---------------------------------------------------------

def generate_response(prompt: str) -> str:
    """
    Sends prompt to Gemini
    and returns AI response.
    """

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        return f"❌ Gemini Error:\n\n{e}"