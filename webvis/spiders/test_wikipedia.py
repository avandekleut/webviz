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


def test_get_first_n():
    spider = WikipediaSpider('wikipedia')

    input = list(range(10))
    n = 3

    first_n = spider.get_first_n(input, n)
    assert first_n == input[:n]
    assert set(first_n) == set(input[:n])
    assert len(first_n) == n
    assert first_n[0] == input[0]


def test_get_first_p():
    spider = WikipediaSpider('wikipedia')

    p = 1/10
    base_length = 32
    input = list(range(int(base_length/p)))

    first_p = spider.get_first_p(input, p)
    assert len(first_p) == base_length
    assert first_p[0] == input[0]


def test_get_any_n():
    spider = WikipediaSpider('wikipedia')

    input = list(range(10))
    n = 3

    any_n = spider.get_any_n(input, n)
    assert len(any_n) == n
    for item in any_n:
        assert item in input


def test_get_any_p():
    spider = WikipediaSpider('wikipedia')

    p = 1/10
    base_length = 32
    input = list(range(int(base_length/p)))

    any_p = spider.get_any_p(input, p)
    assert len(any_p) == base_length
    for item in any_p:
        assert item in input


def test_assert_one_of_many():
    spider = WikipediaSpider('wikipedia')

    exactly_one = [None, 1, None, None]

    assert spider.assert_one_of_many(*exactly_one)

    more_than_one = [None, 1, None, 0.1]

    assert not spider.assert_one_of_many(*more_than_one)

    none = [None, 1, None, 0.1]

    assert not spider.assert_one_of_many(*none)
