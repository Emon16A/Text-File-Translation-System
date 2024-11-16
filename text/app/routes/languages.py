from fastapi import APIRouter
from googletrans import LANGUAGES

# Create a router for handling the languages route
router = APIRouter()

@router.get("/languages")
async def get_languages():
    # Capitalize the first letter of each language name
    capitalized_languages = {key: value.capitalize() for key, value in LANGUAGES.items()}
    return capitalized_languages
