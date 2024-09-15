from flask import render_template
from app import app, db

# Fehlerbehandlungsfunktion für 404-Fehler (Seite nicht gefunden)
@app.errorhandler(404)
def not_found_error(error):
    # Gibt das Template '404.html' zurück und setzt den HTTP-Statuscode auf 404
    return render_template('404.html'), 404

# Fehlerbehandlungsfunktion für 500-Fehler (Interner Serverfehler)
@app.errorhandler(500)
def internal_error(error):
    # Setzt die Datenbank-Session zurück, um einen inkonsistenten Zustand nach einem Fehler zu verhindern
    db.session.rollback()
    # Gibt das Template '500.html' zurück und setzt den HTTP-Statuscode auf 500
    return render_template('500.html'), 500
