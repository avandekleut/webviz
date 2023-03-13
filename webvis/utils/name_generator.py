import json
import hashlib


class NameGenerator:
    @classmethod
    def from_params(cls, **kwargs):
        stringified = json.dumps(kwargs, sort_keys=True)
        encoded = stringified.encode('utf-8')
        hashed = hashlib.md5(encoded).hexdigest()
        return hashed

    @classmethod
    def remove_unsafe_characters(cls, path: str):
        return "".join([c for c in path if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
