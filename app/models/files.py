from app.database import db
from app.utils import wordsplit_pattern

from file_words import FileWords
from words import Word

import boto
from boto.s3.key import Key


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    file_name = db.Column(db.String)
    mime = db.Column(db.String)

    words = db.relationship("Word", secondary=FileWords, backref="files")

    _contents = None
    _s3_conn = None

    def __init__(self, name, mime=''):
        self.name = name
        self.mime = mime

    def __repr__(self):
        return '<File %r: %s>' % (self.id, self.name)

    def __to_json__(self):
        return {
            'id': self.id,
            'name': self.name,
            'file_name': self.file_name,
            'mime': self.mime,
        }

    def process_upload(self, uploaded_file):
        """
        Given an uploaded file object update the state of the model object
        as well as save the contents to the correct location
        """
        self.build_word_assocations(uploaded_file)
        self.store(uploaded_file)

    def build_word_assocations(self, uploaded_file):
        """
        For this file find all the appropriate words and add the relations.
        If re-uploading the file it will remove any stale relations.
        """

        words = self.get_words(self.name) | self.get_words(self.file_name) | \
            self.get_content_words(uploaded_file)

        # Find the words already in the database and then add any missing words
        words_in_db = Word.query.filter(Word.word.in_(words)).all()
        missing_words = words - set(w.word for w in words_in_db)

        self.words = words_in_db + [Word(w) for w in missing_words]

    def get_content_words(self, file_object):
        """
        Given a file like object get the words in the contents if it
        is a text document
        """

        if self.mime != 'text/plain':
            return set()

        self._contents = file_object.read()
        return self.get_words(self._contents)

    def store(self, uploaded_file):
        """Store the file contents on S3"""
        key = self._get_key(self.file_name)
        key.set_contents_from_file(uploaded_file)

    def download_url(self):
        """Get the S3 url for this file"""
        key = self._get_key(self.file_name)
        expires_in = 60  # Number of seconds this url is valid for
        return key.generate_url(expires_in)

    @classmethod
    def find_or_create(cls, name, mime=''):
        """Find an existing file by name or create it if not found"""
        return cls.query.filter(cls.name == name).first() or cls(name, mime)

    @staticmethod
    def get_words(contents):
        """For a string break it out into words"""
        return set(w.lower() for w in wordsplit_pattern.findall(contents))

    @classmethod
    def number_of_files(cls):
        """Return the number of files in the database"""
        return db.session.query(db.func.count(cls.id)).first()[0]

    @classmethod
    def _get_s3_bucket(cls):
        """Get the S3 bucket"""
        if not cls._s3_conn:
            cls._s3_conn = boto.connect_s3()

        return cls._s3_conn.get_bucket('fablelabs')

    @classmethod
    def _get_key(cls, filename):
        """Get a S3 key for the filename."""
        bucket = cls._get_s3_bucket()
        key = bucket.get_key(filename)

        if key is None:
            key = Key(bucket)
            key.key = filename

