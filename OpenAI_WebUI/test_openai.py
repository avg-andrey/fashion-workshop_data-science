# test_openai.py

import os
from openai import OpenAI
import logging
import sys

# Configure logging for debugging
# Set stdout encoding on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Set up logging
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logging.basicConfig(level=logging.DEBUG, handlers=[handler])

logging.debug("Logging has been successfully configured!")

# Retrieve the API key from the environment variable
api_key = "000000000000000000000000000"

try:
    # Initialize OpenAI client
    client = OpenAI(
        api_key=api_key
    )
    
    # Call the Chat Completions API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    print("==== RESPONSE ====")
    print(response.choices[0].message.content.strip())

except Exception as e:
    logging.error(f"OpenAI API error: {str(e)}", exc_info=True)
