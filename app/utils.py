from flask.json import JSONEncoder
import re

wordsplit_pattern = re.compile(r'[^\s!,.?":;0-9]+')


class AppJsonEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__to_json__'):
            return obj.__to_json__()

        return JSONEncoder.default(self, obj)
