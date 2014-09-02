from app.utils import wordsplit_pattern

from app.models.files import File
from app.models.words import Word

from flask import redirect, request, jsonify


def publish():
    """
    From a multipart/form-data request add or update a file in the system
    """
    name = request.form.get('name')
    uploaded_file = request.files['file']
    mime = uploaded_file.content_type

    file = File.find_or_create(name, mime)
    file.file_name = uploaded_file.filename
    file.process_upload(uploaded_file)

    # Allow the endpoint to be called directly from the browser
    if 'browser' in request.args:
        return redirect('/upload?success=true')

    return jsonify(file=file)


def search(text=None):
    """
    Search the files for a set of words and return any matches.
    If no search terms are given then return all files.
    """

    if text:
        # Split the text into individual words
        individual_words = wordsplit_pattern.findall(text)

        file_matches = {}

        # Find the words that match and then get the files for that word
        words = Word.search(individual_words)

        for word in words:
            for file in word.files:
                if file.name not in file_matches:
                    file_matches[file.name] = file

        files = file_matches.values()
    else:
        files = File.query.all()

    return jsonify(files=files)


def get_file(id):
    """Download the file with the given id"""
    file = File.query.get_or_404(id)
    return redirect(file.download_url())
