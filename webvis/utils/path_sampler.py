class PathSampler:
    def __init__(self, branching_factor: int):
        self.branching_factor = branching_factor

    def filter(self, urls):
        urls = self._get_unique(urls)
        urls = self._select_subset(urls)
        return urls

    def _get_unique(self, urls: list):
        return list(dict.fromkeys(urls))

    def _select_subset(self, urls: list):
        return urls[:self.branching_factor]
