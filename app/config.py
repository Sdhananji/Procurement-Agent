import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")



# How much each factor matters when ranking suppliers. Must add up to 1.0.
SCORING_WEIGHTS = {
    "price": 0.5,
    "delivery": 0.3,
    "reliability": 0.2,
}