from app.database import db


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, unique=True)

    def __init__(self, word, mime=''):
        self.word = word

    def __repr__(self):
        return '<Word %r: %s>' % (self.id, self.word)

    @classmethod
    def find_or_create(cls, word):
        """Find an existing word or create it if not found"""
        return cls.query.filter(cls.word == word).first() or cls(word)

    @classmethod
    def number_of_words(cls):
        """Return the number of words in the database"""
        return db.session.query(db.func.count(cls.id)).first()[0]

    @classmethod
    def search(cls, terms):
        """Find all words in the database that are in the list of terms"""
        return cls.query.filter(cls.word.in_(terms)).all()
