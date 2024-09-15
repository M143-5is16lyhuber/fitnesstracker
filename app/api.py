from flask import Blueprint, g, request
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, login_required
from app.models import User, Post, Calendar, PlannedTraining

# Erstelle ein Blueprint für die API und initialisiere Flask-Restful API und HTTP-Auth
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
auth = HTTPBasicAuth()

# Verifikation der Benutzerauthentifizierung
@auth.verify_password
def verify_password(username, password):
    # Suche den Benutzer in der Datenbank basierend auf dem Benutzernamen
    user = User.query.filter_by(username=username).first()
    # Wenn der Benutzer existiert und das Passwort korrekt ist, setze den Benutzer als aktuellen Benutzer
    if user and user.check_password(password):
        g.current_user = user  # Speichere den Benutzer in der globalen Flask-Variable
        return user
    return None  # Rückgabe None, wenn die Authentifizierung fehlschlägt

# API-Ressource für das Dashboard
class DashboardResource(Resource):
    @auth.login_required  # Authentifizierung ist erforderlich, um auf die Ressource zuzugreifen
    def get(self):
        # Hol den authentifizierten Benutzer
        user = g.current_user
        # Hol alle Posts (Trainingseinheiten) des Benutzers
        posts = Post.query.filter_by(user_id=user.id).all()
        # Berechne die Gesamtminuten der Trainingseinheiten
        total_minutes = sum(post.duration for post in posts)
        # Rückgabe der Gesamtminuten im JSON-Format
        return {'total_minutes': total_minutes}

# API-Ressource für die Kalendereinträge des Benutzers
class UserCalendarEntriesResource(Resource):
    @auth.login_required  # Authentifizierung ist erforderlich, um auf die Ressource zuzugreifen
    def get(self):
        # Hol den authentifizierten Benutzer
        user = g.current_user
        # Hol alle geplanten Trainingseinträge des Benutzers aus dem Kalender
        calendar_entries = PlannedTraining.query.filter_by(user_id=user.id).all()
        # Rückgabe einer Liste der Kalendereinträge im JSON-Format
        return [{
            'id': entry.id,
            'title': entry.title,
            'description': entry.description,
            'date': entry.date.isoformat(),  # Konvertiere das Datum in einen String
            'time': entry.time.isoformat() if entry.time else None,  # Konvertiere die Zeit in einen String, falls vorhanden
            'activity_type': entry.activity_type  # Typ der Aktivität (z.B. Laufen, Krafttraining)
        } for entry in calendar_entries]

# Füge die Ressourcen (Routen) für die API hinzu
api.add_resource(DashboardResource, '/dashboard')
api.add_resource(UserCalendarEntriesResource, '/calendar')
