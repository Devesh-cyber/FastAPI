from dotenv import load_dotenv
import os

MONGODB_URI='mongodb://root:mypassword@localhost:27017/'
ALLOWED_EXTENSIONS = ['.pdf','.txt']
UPLOAD_DIR = 'uploads'
MAX_SIZE_IN_MB = 10

GEMINI_API_KEY = os.getenv('GOOGLE_AI_API_KEY')