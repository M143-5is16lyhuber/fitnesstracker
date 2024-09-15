from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialisiere die Flask-Anwendung
app = Flask(__name__)

# Lade die Konfiguration aus dem Config-Objekt
app.config.from_object(Config)

# Initialisiere die SQLAlchemy-Datenbank
db = SQLAlchemy(app)

# Initialisiere Flask-Migrate für die Verwaltung von Datenbankmigrationen
migrate = Migrate(app, db)

# Initialisiere Flask-Login für die Benutzer-Authentifizierung
login = LoginManager(app)

# Bestimme die Login-Route, auf die nicht-authentifizierte Benutzer weitergeleitet werden
login.login_view = 'login'

# Importiere Routen, Modelle und Fehlerbehandlungslogik der Anwendung
from app import routes, models, errors
from app.api import api_bp

# Wenn die Anwendung nicht im Debug-Modus läuft
if not app.debug:
    # Überprüfe, ob das Logs-Verzeichnis existiert, erstelle es falls nötig
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Erstelle einen RotatingFileHandler für die Logdatei mit einer Maximalgröße von 10 MB und maximal 10 Backup-Dateien
    file_handler = RotatingFileHandler('logs/fitnesstracker.log', maxBytes=10240,
                                       backupCount=10)
    
    # Setze das Logformat mit Zeitstempel, Log-Level, Nachricht und Dateipfad/Zeilennummer
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    
    # Setze das Log-Level auf INFO, um alle Logs ab dieser Ebene zu erfassen
    file_handler.setLevel(logging.INFO)
    
    # Füge den File-Handler zur Logger-Instanz der Anwendung hinzu
    app.logger.addHandler(file_handler)

    # Setze das allgemeine Log-Level der Anwendung auf INFO
    app.logger.setLevel(logging.INFO)
    
    # Logge die Nachricht, dass die Anwendung gestartet wurde
    app.logger.info('FitnessTracker startup')

# Importiere Routen, Modelle und Fehler erneut (redundanter Import, aber keine Codeänderung wie gewünscht)
from app import routes, models, errors
from app.api import api_bp

# Registriere das Blueprint für die API und setze das URL-Präfix auf '/api'
app.register_blueprint(api_bp, url_prefix='/api')
