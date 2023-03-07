from webvis.spiders.wikipedia import WikipediaSpider


def test_wildcard_to_regular_expression():
    spider = WikipediaSpider('wikipedia')

    input = 'abc*'
    expected = 'abc.+'

    result = spider.wildcard_to_regular_expression(input)

    assert result == expected, f'{result} != {expected}'

    # assert 1 == 2


def test__ignore_bad_path():
    spider = WikipediaSpider('wikipedia')

    inputs = ['https://en.wikipedia.org/wiki/Category:Wikipedia_tutorials',
              'https://en.wikipedia.org/wiki/Category:Luxembourg%E2%80%93Spain_relations']

    for input in inputs:
        assert spider.should_ignore_path(input)


def test_ignore_bad_path():
    spider = WikipediaSpider('wikipedia')

    input = 'https://en.wikipedia.org/wiki/Continuous_Function'

    assert spider.should_allow_path(input)
