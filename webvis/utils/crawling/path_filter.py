import re


class PathFilter:
    def __init__(self,
                 allowed_paths: "list[str]" or None,
                 ignore_paths: "list[str]" or None
                 ):
        self.allowed_paths = allowed_paths or ['*']
        self.ignore_paths = ignore_paths or []

        self.visited = []

    def visit(self, url):
        self.visited.append(url)

    def should_allow(self, url):
        return not self.should_ignore(url)

    def should_ignore(self, url):
        if url in self.visited:
            return True

        if self.should_ignore_path(url):
            return True

        if not self.should_allow_path(url):
            return True

    def should_ignore_path(self, path):
        return self.filter_paths_by_pattern(path, self.ignore_paths)

    def should_allow_path(self, path):
        return self.filter_paths_by_pattern(path, self.allowed_paths)

    def filter_paths_by_pattern(self, path, patterns):
        for pattern in patterns:
            regular_expression = self.wildcard_to_regular_expression(pattern)
            if re.match(regular_expression, path):
                return True

        return False

    def wildcard_to_regular_expression(self, path):
        return re.escape(path).replace('\\*', '.+')
