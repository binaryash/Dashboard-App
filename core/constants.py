import os
from dotenv import load_dotenv

# Go one directory up from the current script directory
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
