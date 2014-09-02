from flask import render_template
from app.models import files, words


def index():
    number_of_files = files.File.number_of_files()
    number_of_words = words.Word.number_of_words()

    params = {
        'file_count': number_of_files,
        'word_count': number_of_words,
    }

    return render_template('index.html', **params)


def upload():
    return render_template('upload.html')


def search():
    return render_template('search.html')
