import argparse
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if api_key is None:
    raise RuntimeError("Gemini API key not found!")

parser = argparse.ArgumentParser(description="AI-Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=args.user_prompt,
)
print("Response:")
if response.usage_metadata is None:
    raise RuntimeError(
        "Gemini API response missing usage metadata; token usage could not be determined."
    )
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)
