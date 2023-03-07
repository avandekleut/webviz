from webvis.spiders.wikipedia import WikipediaSpider


def test_wildcard_to_regular_expression():
    spider = WikipediaSpider('wikipedia')

    input = 'abc*'
    expected = 'abc.+'

    result = spider.wildcard_to_regular_expression(input)

    assert result == expected, f'{result} != {expected}'
