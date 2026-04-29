from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path

# ✅ Load .env from project root (fix for Streamlit path issue)
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# ✅ Initialize AFTER loading env
client = Groq(api_key=api_key)


def generate_summary(insights):
    """
    Convert structured insights into human-readable business summary using Groq (Llama3)
    """

    if not insights:
        return "No significant insights found."

    # Convert insights to text
    insights_text = ""
    for ins in insights:
        insights_text += (
            f"- {ins.text} | Priority: {ins.priority} | Action: {ins.action}\n"
        )

    prompt = f"""
You are a senior business analyst.

Generate a concise executive summary (5–6 lines max).

Focus on:
- Key changes
- Important anomalies
- Business impact
- Recommended actions

Insights:
{insights_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert business analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating summary: {str(e)}"