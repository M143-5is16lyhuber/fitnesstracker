import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post

# Diese Funktion wird verwendet, um zusätzliche Objekte im Flask-Shell-Kontext verfügbar zu machen.
@app.shell_context_processor
def make_shell_context():
    # Hier werden das SQLAlchemy-Modul (sa), der SQLAlchemy-ORM (so), die Datenbankinstanz (db),
    # sowie die Modelle User und Post im Shell-Kontext verfügbar gemacht.
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
