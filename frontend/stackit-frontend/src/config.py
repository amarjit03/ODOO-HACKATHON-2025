import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdf#FGSgvasgf$5$WGT'
    API_BASE_URL = os.environ.get('API_BASE_URL') or 'http://3.82.218.27'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

