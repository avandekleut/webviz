class PathSampler:
    def __init__(self, branching_factor: int):
        self.branching_factor = branching_factor

    def filter(self, urls):
        urls = self.get_unique(urls)
        urls = self.select_subset(urls)
        return urls

    def get_unique(self, urls: list):
        return list(dict.fromkeys(urls))

    def select_subset(self, urls: list):
        return urls[:self.branching_factor]
