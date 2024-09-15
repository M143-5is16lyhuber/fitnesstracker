from app import login
from datetime import datetime, timezone
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# Funktion, die verwendet wird, um Benutzer basierend auf der ID zu laden
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# Tabelle für das Verfolgen von Benutzerbeziehungen (Follower und Gefolgte)
followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True)
)

# Benutzerklasse, die UserMixin für die Login-Verwaltung und SQLAlchemy für die Datenbankintegration verwendet
class User(UserMixin, db.Model):
    # Benutzer-ID als Primärschlüssel
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # Benutzername, einzigartig und indiziert
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    # E-Mail-Adresse, einzigartig und indiziert
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    # Passwort-Hash für die Authentifizierung
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # Beziehung zu den Posts, die der Benutzer erstellt hat
    posts: so.Mapped[List['Post']] = so.relationship('Post', back_populates='author', lazy='dynamic')
    # Optionales Feld für die "Über mich"-Beschreibung des Benutzers
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    # Letztes Login-Datum des Benutzers
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    
    # Beziehung zu den Benutzern, denen der aktuelle Benutzer folgt
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id), back_populates='followers')
    
    # Beziehung zu den Benutzern, die dem aktuellen Benutzer folgen
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id), back_populates='following')

    # Repräsentation des Benutzers als String
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Funktion, um das Passwort zu setzen (verschlüsselt es)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Funktion, um das Passwort zu überprüfen
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Funktion, um den Gravatar-Avatar des Benutzers zu generieren
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # Funktion, um einem anderen Benutzer zu folgen
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    # Funktion, um einem Benutzer nicht mehr zu folgen
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    # Überprüfung, ob der aktuelle Benutzer einem anderen Benutzer folgt
    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    # Anzahl der Follower
    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(self.followers.select().subquery())
        return db.session.scalar(query)

    # Anzahl der Benutzer, denen der aktuelle Benutzer folgt
    def following_count(self):
        query = sa.select(sa.func.count()).select_from(self.following.select().subquery())
        return db.session.scalar(query)

    # Funktion, um alle Posts der Benutzer, denen der aktuelle Benutzer folgt, abzurufen
    def following_posts(self):
        Author = so.aliased(User)  # Alias für die Autoren
        Follower = so.aliased(User)  # Alias für die Follower
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(sa.or_(Follower.id == self.id, Author.id == self.id))
            .group_by(Post)
            .order_by(Post.timestamp.desc())
        )

# Klasse für Posts (z.B. Trainingsberichte)
class Post(db.Model):
    # Primärschlüssel für den Post
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # Textinhalt des Posts (max. 140 Zeichen)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    # Zeitstempel des Posts
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    # Fremdschlüssel zur Benutzer-ID
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'),
                                               index=True)
    # Beziehung zum Autor (Benutzer)
    author: so.Mapped['User'] = so.relationship('User', back_populates='posts')
    # Typ der Aktivität (z.B. Laufen, Krafttraining)
    activity_type: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    # Dauer der Aktivität in Minuten
    duration: so.Mapped[int] = so.mapped_column(nullable=False)

    # Repräsentation des Posts als String
    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Klasse für Kalendereinträge
class Calendar(db.Model):
    # Primärschlüssel für den Kalendereintrag
    id = db.Column(db.Integer, primary_key=True)
    # Titel des Kalendereintrags
    title = db.Column(db.String(64), nullable=False)
    # Beschreibung des Kalendereintrags
    description = db.Column(db.String(140), nullable=True)
    # Datum des Kalendereintrags
    date = db.Column(db.Date, nullable=False)
    # Fremdschlüssel zur Benutzer-ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Repräsentation des Kalendereintrags als String
    def __repr__(self):
        return f'<Calendar {self.title}>'
    
# Klasse für geplante Trainingseinheiten
class PlannedTraining(db.Model):
    # Primärschlüssel für die Trainingseinheit
    id = db.Column(db.Integer, primary_key=True)
    # Fremdschlüssel zur Benutzer-ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Titel der Trainingseinheit
    title = db.Column(db.String(64), nullable=False)
    # Beschreibung der Trainingseinheit
    description = db.Column(db.String(140), nullable=True)
    # Datum der Trainingseinheit
    date = db.Column(db.Date, nullable=False)
    # Zeit der Trainingseinheit
    time = db.Column(db.Time, nullable=False)
    # Art der Aktivität (z.B. Laufen, Fahrradfahren, Krafttraining)
    activity_type = db.Column(db.String(64), nullable=False)

    # Repräsentation der geplanten Trainingseinheit als String
    def __repr__(self):
        return f'<PlannedTraining {self.title}>'
