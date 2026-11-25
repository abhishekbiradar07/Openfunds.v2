import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api/v1')

# App Configuration
APP_TITLE = "OpenFunds"
APP_ICON = "💰"
APP_LAYOUT = "wide"

# API Timeouts (seconds)
API_TIMEOUT = 30
API_RETRY_ATTEMPTS = 3
API_RETRY_DELAY = 2  # seconds
