import os
from dotenv import load_dotenv

load_dotenv('credentials.env')

FAB_API_URL = os.getenv("FAB_API_URL")
FAB_USER_ID = os.getenv("FAB_USER_ID")
FAB_API_KEY = os.getenv("FAB_API_KEY")
