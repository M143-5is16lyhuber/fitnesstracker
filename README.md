# Fitness Tracker Anwendung für VCID

Dies ist eine webbasierte Anwendung auf Flask-Basis zum Verfolgen verschiedener Fitnessaktivitäten. Benutzer können sich anmelden, ihre Workouts protokollieren, ihren Trainingsverlauf anzeigen und anderen Benutzern folgen. Die Anwendung bietet zudem ein Dashboard zur Visualisierung der gesamten Trainingszeit und der Aufschlüsselung der Aktivitäten.

## Funktionen

- **Benutzerregistrierung & Authentifizierung**: Benutzer können sich registrieren, anmelden und abmelden.
- **Aktivitätsverfolgung**: Protokollieren Sie verschiedene Arten von Aktivitäten wie Laufen, Radfahren und Krafttraining.
- **Benutzerprofile**: Sehen Sie sich Ihr Profil an und bearbeiten Sie persönliche Informationen.
- **Folgen**: Folgen Sie anderen Benutzern, um über deren Aktivitäten auf dem Laufenden zu bleiben.
- **Dashboard**: Visualisieren Sie die gesamte Trainingszeit und die Aufschlüsselung nach Aktivitätstypen.
- **Kalender**: Planen und terminieren Sie Ihre kommenden Workouts mit der Kalenderfunktion.
- **Erkunden**: Entdecken Sie Aktivitäten anderer Benutzer.

## Anforderungen

Das `setup.sh`-Skript wird die folgenden Requirements installieren:

- Python-Module
- MySQL
- Nginx
- Gunicorn
- Supervisor

## Installation

1. **Laden Sie das `setup.sh`-Skript herunter**:

   ```bash
   wget https://raw.githubusercontent.com/M143-5is16lyhuber/fitnesstracker/master/setup.sh

2. **Führen Sie das Skript aus**:

   ```bash
    chmod +x setup.sh
   ./setup.sh

3. **Verbinden Sie sich über die IP-Adresse mit Ihrem Webserver**:

   ```bash
   http://<your-ip>
