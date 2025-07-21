from dotenv import load_dotenv
import os


load_dotenv('.env')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

URL_DATABASE = os.getenv("URL_DATABASE")
if URL_DATABASE is None:
    raise ValueError("URL_DATABASE is not set")

