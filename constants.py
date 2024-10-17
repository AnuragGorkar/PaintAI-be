from dotenv import load_dotenv
import os

# Load .env in local development
load_dotenv()

# Get variables from environment or set default values
SERVER_URL = os.getenv('SERVER_URL', 'localhost')
PORT = os.getenv('PORT', '8900')
ENV = os.getenv('ENV', 'dev')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")