from sqlalchemy.dialects.mysql import TEXT

from .db import db


class Song(db.Model):  # type: ignore
    __tablename__ = "song"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(TEXT)
    artist = db.Column(TEXT)
    url = db.Column(TEXT, nullable=True)

    def __init__(self, title, artist, url=None):
        self.title = title
        self.artist = artist
        self.url = url

    def __repr__(self):
        return (
            f"<id: {self.id}, title: {self.title}, artist: {self.artist}, url:"
            f" {self.url}>"
        )

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "url": self.url,
        }
