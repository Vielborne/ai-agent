import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from a .env file
load_dotenv()
# Retrieve the Gemini API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
# Initialize the Gemini API client with the API key
client = genai.Client(api_key=api_key)

# If API key not found; raise an error
if api_key is None:
    raise RuntimeError("Gemini API key not found!")

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="AI-Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Format the user's prompt into the message structure expected by the Gemini API
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

# Send the prompt to the Gemini API and get a response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
)

# If verbose mode is enabled, display additional metadata about the request
if args.verbose is True:
    print(f"User prompt: {args.user_prompt}")
    # Ensure usage metadata is present before accessing token counts
    if response.usage_metadata is None:
        raise RuntimeError(
            "Gemini API response missing usage metadata; token usage could not be determined."
        )
    # Display token usage statistics
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)
else:
    # In non-verbose mode, just print the response
    print("Response:")
    print(response.text)
