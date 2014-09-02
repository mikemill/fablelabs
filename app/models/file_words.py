from app.database import db


# The many-to-many relationship table between files and words
FileWords = db.Table(
    'file_words',

    db.Column('file_id', db.Integer,
              db.ForeignKey('files.id'), primary_key=True),

    db.Column('word_id', db.Integer,
              db.ForeignKey('words.id'), primary_key=True)
)
