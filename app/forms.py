from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, TimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User
from wtforms import TextAreaField
from wtforms.validators import Length
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length

# Formular für die Benutzeranmeldung
class LoginForm(FlaskForm):
    # Feld für den Benutzernamen, Eingabe erforderlich
    username = StringField('Username', validators=[DataRequired()])
    # Feld für das Passwort, Eingabe erforderlich
    password = PasswordField('Password', validators=[DataRequired()])
    # Checkbox zum Merken der Anmeldung
    remember_me = BooleanField('Remember Me')
    # Senden-Button
    submit = SubmitField('Sign In')

# Formular für die Benutzerregistrierung
class RegistrationForm(FlaskForm):
    # Feld für den Benutzernamen, Eingabe erforderlich
    username = StringField('Username', validators=[DataRequired()])
    # Feld für die E-Mail, Eingabe erforderlich und muss eine gültige E-Mail sein
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Feld für das Passwort, Eingabe erforderlich
    password = PasswordField('Password', validators=[DataRequired()])
    # Wiederholung des Passworts, muss mit dem ersten Passwort übereinstimmen
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # Senden-Button
    submit = SubmitField('Register')

    # Validierung, um sicherzustellen, dass der Benutzername nicht bereits verwendet wird
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Validierung, um sicherzustellen, dass die E-Mail nicht bereits verwendet wird
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Formular zur Bearbeitung des Benutzerprofils
class EditProfileForm(FlaskForm):
    # Feld für den Benutzernamen, Eingabe erforderlich
    username = StringField('Username', validators=[DataRequired()])
    # Textfeld für die "Über mich"-Beschreibung, max. 140 Zeichen
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    # Senden-Button
    submit = SubmitField('Submit')

    # Initialisiere das Formular und speichere den ursprünglichen Benutzernamen
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    # Validierung, um sicherzustellen, dass der neue Benutzername nicht bereits verwendet wird
    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')

# Leeres Formular für einfache Formulare mit nur einem Senden-Button
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# Formular für Posts (z.B. Trainingseinträge)
class PostForm(FlaskForm):
    # Textfeld für den Post-Inhalt, Eingabe erforderlich, max. 140 Zeichen
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    # Dropdown-Menü zur Auswahl der Aktivitätsart, Eingabe erforderlich
    activity_type = SelectField('Activity Type', choices=[('Laufen', 'Laufen'), ('Fahrradfahren', 'Fahrradfahren'), ('Krafttraining', 'Krafttraining')], validators=[DataRequired()])
    # Feld für die Trainingsdauer in Minuten, Eingabe erforderlich
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    # Senden-Button
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

# Formular für Kalendereinträge
class CalendarForm(FlaskForm):
    # Feld für den Titel des Eintrags, Eingabe erforderlich
    title = StringField('Title', validators=[DataRequired()])
    # Textfeld für die Beschreibung des Eintrags (optional)
    description = TextAreaField('Description')
    # Datumsfeld für den Kalendereintrag, Eingabe erforderlich
    date = DateField('Date', validators=[DataRequired()])
    # Senden-Button
    submit = SubmitField('Submit')

# Formular zur Planung von Trainingseinheiten
class PlanTrainingForm(FlaskForm):
    # Feld für den Titel der Trainingseinheit, Eingabe erforderlich
    title = StringField('Title', validators=[DataRequired()])
    # Textfeld für die Beschreibung der Einheit (optional)
    description = TextAreaField('Description')
    # Datumsfeld für das geplante Datum, Eingabe erforderlich
    date = DateField('Date', validators=[DataRequired()])
    # Zeitfeld für die geplante Zeit, Eingabe erforderlich
    time = TimeField('Time', validators=[DataRequired()])
    # Dropdown-Menü zur Auswahl der Aktivitätsart, Eingabe erforderlich
    activity_type = SelectField('Activity Type', choices=[('Laufen', 'Laufen'), ('Krafttraining', 'Krafttraining'), ('Fahrradfahren', 'Fahrradfahren')], validators=[DataRequired()])
    # Senden-Button
    submit = SubmitField('Plan Training')
