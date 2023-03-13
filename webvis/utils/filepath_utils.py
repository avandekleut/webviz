class FilepathUtils:
    @classmethod
    def generate_filepath(cls, **kwargs):
        parts = []
        for key, value in kwargs.items():
            parts.append(f'{key} {value}')
        combined = " ".join(parts)

        return cls.safe_filepath(combined)

    @classmethod
    def safe_filepath(cls, path: str):
        return "".join([c for c in path if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
