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
=======
# Fitness Tracker Application for VCID

This is a Flask-based web application for tracking various fitness activities. Users can log in, track their workouts, view their training history, follow other users, and explore new fitness trends. The application also provides a dashboard for visualizing total workout time and activity breakdown.

## Features

- **User Registration & Authentication**: Users can sign up, log in, and log out.
- **Activity Tracking**: Log different types of activities such as running, cycling, and strength training.
- **User Profiles**: View your profile and edit personal information.
- **Following**: Follow other users to keep up with their activities.
- **Dashboard**: Visualize the total workout time and breakdown by activity type.
- **Calendar**: Plan and schedule your upcoming workouts using the calendar feature.
- **Explore**: Discover activities from other users.

## Requirements

The setup.sh script will install the following requirements:

- Python Modules
- MySQL 
>>>>>>> e636cbf (Final Commit)
- Nginx
- Gunicorn
- Supervisor

## Installation

<<<<<<< HEAD
1. **Laden Sie das `setup.sh`-Skript herunter**:

   ```bash
   wget https://raw.githubusercontent.com/M143-5is16lyhuber/fitnesstracker/master/setup.sh

2. **Führen Sie das Skript aus**:

   ```bash
    chmod +x setup.sh
   ./setup.sh

4. **Verbinden Sie sich über die IP-Adresse mit Ihrem Webserver**:

   ```bash
   http://<your-ip>
=======
1. **Clone the repository**:

   ```bash
   git clone https://github.com/M143-5is16lyhuber/fitnesstracker/.git
   cd fitnesstracker

2. ** Run the script**:

    ```bash
   ./setup.sh

3. ** Connect to your Web-Server over the IP **

   ```bash
   http://<your-ip>

>>>>>>> e636cbf (Final Commit)
