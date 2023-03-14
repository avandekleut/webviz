from webvis.utils.crawling.path_filter import PathFilter


class WikipediaPathFilter(PathFilter):
    def __init__(self,):
        super().__init__(
            allowed_paths=[
                "https://en.wikipedia.org/wiki/*",
            ],
            ignore_paths=[
                # discussion posts etc
                "https://en.wikipedia.org/wiki/*:*",

                # keep search local, main page links to random
                "https://en.wikipedia.org/wiki/Main_Page"
            ]
        )
