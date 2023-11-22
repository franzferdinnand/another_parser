import pytesseract
from PIL import Image


def fetch_email_from_pic(img) -> str:
    return pytesseract.image_to_string(Image.open(img))
