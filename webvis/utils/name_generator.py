class NameGenerator:
    @classmethod
    def from_params(cls, **kwargs):
        parts = []
        for key, value in kwargs.items():
            parts.append(f'{key} {value}')
        combined = " ".join(parts)

        return cls.remove_unsafe_characters(combined)

    @classmethod
    def remove_unsafe_characters(cls, path: str):
        return "".join([c for c in path if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
