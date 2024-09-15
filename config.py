import os
from dotenv import load_dotenv

# Bestimme das Basisverzeichnis der Anwendung
basedir = os.path.abspath(os.path.dirname(__file__))

# Lade Umgebungsvariablen aus der .env-Datei, die im Basisverzeichnis liegt
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # SECRET_KEY wird verwendet, um wichtige Daten wie Sitzungen und Cookies zu sichern
    # Es wird zuerst versucht, den Wert aus den Umgebungsvariablen zu laden, sonst wird ein Standardwert verwendet
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'FlaskPassword1'
    
    # SQLALCHEMY_DATABASE_URI enthält die Datenbankverbindung
    # Sie wird ebenfalls aus den Umgebungsvariablen geladen
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Anzahl der Posts, die pro Seite bei der Paginierung angezeigt werden sollen
    POSTS_PER_PAGE = 5
