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

    inputs = [
        'https://en.wikipedia.org/wiki/Category:Wikipedia_tutorials',
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

    p = 1 / 10
    base_length = 32
    input = list(range(int(base_length / p)))

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

    p = 1 / 10
    base_length = 32
    input = list(range(int(base_length / p)))

    any_p = spider.get_any_p(input, p)
    assert len(any_p) == base_length
    for item in any_p:
        assert item in input


def test_outgoing_links_hardocded():
    outgoing_links = [
        'http://calphotos.berkeley.edu/cgi/img_query?where-taxon=Salix+bebbiana',
        'http://etsetoninstitute.org/wp-content/uploads/2012/09/The_Arctic_Prairies.pdf',
        'http://legacy.tropicos.org/Name/28300022',
        'http://www.efloras.org/florataxon.aspx?flora_id=1&taxon_id=242445657',
        'http://www.fs.fed.us/database/feis/plants/tree/salbeb/all.html',
        'http://www.pfaf.org/user/Plant.aspx?LatinName=Salix+bebbiana',
        'http://www.theplantlist.org/tpl1.1/record/kew-5001777',
        'http://www.worldfloraonline.org/taxon/wfo-0000929260',
        'https://apiv3.iucnredlist.org/api/v3/taxonredirect/64324259',
        'https://az.wikipedia.org/wiki/Bebb_s%C3%B6y%C3%BCd%C3%BC',
        'https://ceb.wikipedia.org/wiki/Salix_bebbiana',
        'https://commons.wikimedia.org/wiki/Category:Salix_bebbiana',
        'https://creativecommons.org/licenses/by-sa/3.0/',
        'https://data.canadensys.net/vascan/taxon/9079',
        'https://developer.wikimedia.org',
        'https://donate.wikimedia.org/wiki/Special:FundraiserRedirector?utm_source=donate&utm_medium=sidebar&utm_campaign=C13_en.wikipedia.org&uselang=en',
        'https://en.m.wikipedia.org/w/index.php?title=Salix_bebbiana&mobileaction=toggle_view_mobile',
        'https://en.wikipedia.org/w/index.php?title=Salix_bebbiana&action=edit',
        'https://en.wikipedia.org/w/index.php?title=Salix_bebbiana&action=edit&section=1',
        'https://en.wikipedia.org/w/index.php?title=Salix_bebbiana&action=edit&section=2',
        'https://en.wikipedia.org/w/index.php?title=Salix_bebbiana&action=history',
        'https://en.wikipedia.org/w/index.php?title=Salix_bebbiana&action=info',
        'https://en.wikipedia.org/w/index.php?title=Salix_bebbiana&oldid=1094751939',
        'https://en.wikipedia.org/w/index.php?title=Salix_bebbiana&printable=yes',
        'https://en.wikipedia.org/w/index.php?title=Special:CiteThisPage&page=Salix_bebbiana&id=1094751939&wpFormIdentifier=titleform',
        'https://en.wikipedia.org/w/index.php?title=Special:CreateAccount&returnto=Salix+bebbiana',
        'https://en.wikipedia.org/w/index.php?title=Special:DownloadAsPdf&page=Salix_bebbiana&action=show-download-screen',
        'https://en.wikipedia.org/w/index.php?title=Special:UserLogin&returnto=Salix+bebbiana',
        'https://en.wikipedia.org/wiki/Alaska',
        'https://en.wikipedia.org/wiki/Arizona',
        'https://en.wikipedia.org/wiki/Arrow',
        'https://en.wikipedia.org/wiki/Basket_weaving',
        'https://en.wikipedia.org/wiki/Binomial_nomenclature',
        'https://en.wikipedia.org/wiki/Biological_dispersal',
        'https://en.wikipedia.org/wiki/Bog',
        'https://en.wikipedia.org/wiki/CalPhotos',
        'https://en.wikipedia.org/wiki/California',
        'https://en.wikipedia.org/wiki/California_Native_Plant_Society',
        'https://en.wikipedia.org/wiki/Canada',
        'https://en.wikipedia.org/wiki/Catalogue_of_Life',
        'https://en.wikipedia.org/wiki/Category:Articles_with_%27species%27_microformats',
        'https://en.wikipedia.org/wiki/Category:Articles_with_short_description',
        'https://en.wikipedia.org/wiki/Category:Commons_category_link_from_Wikidata',
        'https://en.wikipedia.org/wiki/Category:Flora_of_Alaska',
        'https://en.wikipedia.org/wiki/Category:Flora_of_California',
        'https://en.wikipedia.org/wiki/Category:Flora_of_Eastern_Canada',
        'https://en.wikipedia.org/wiki/Category:Flora_of_Western_Canada',
        'https://en.wikipedia.org/wiki/Category:Flora_of_the_Great_Lakes_region_(North_America)',
        'https://en.wikipedia.org/wiki/Category:Flora_of_the_North-Central_United_States',
        'https://en.wikipedia.org/wiki/Category:Flora_of_the_Northeastern_United_States',
        'https://en.wikipedia.org/wiki/Category:Flora_of_the_Northwestern_United_States',
        'https://en.wikipedia.org/wiki/Category:Flora_of_the_Southwestern_United_States',
        'https://en.wikipedia.org/wiki/Category:Flora_without_expected_TNC_conservation_status',
        'https://en.wikipedia.org/wiki/Category:Plants_described_in_1895',
        'https://en.wikipedia.org/wiki/Category:Salix',
        'https://en.wikipedia.org/wiki/Category:Short_description_is_different_from_Wikidata',
        'https://en.wikipedia.org/wiki/Category:Taxonbars_with_25%E2%80%9329_taxon_IDs',
        'https://en.wikipedia.org/wiki/Category:Trees_of_the_Northeastern_United_States',
        'https://en.wikipedia.org/wiki/Catkin',
        'https://en.wikipedia.org/wiki/Cattle',
        'https://en.wikipedia.org/wiki/Charles_Sprague_Sargent',
        'https://en.wikipedia.org/wiki/Clay',
        'https://en.wikipedia.org/wiki/Cloning',
        'https://en.wikipedia.org/wiki/Diamond_willow',
        'https://en.wikipedia.org/wiki/EPPO_Code',
        'https://en.wikipedia.org/wiki/Encyclopedia_of_Life',
        'https://en.wikipedia.org/wiki/Eudicots',
        'https://en.wikipedia.org/wiki/File:Commons-logo.svg',
        'https://en.wikipedia.org/wiki/File:S_bebbinia.jpg',
        'https://en.wikipedia.org/wiki/File:Salix_bebbiana.jpg',
        'https://en.wikipedia.org/wiki/File:Salix_bebbiana_(5027584564).jpg',
        'https://en.wikipedia.org/wiki/File:Salix_bebbiana_range_map_1.png',
        'https://en.wikipedia.org/wiki/Flora_of_North_America',
        'https://en.wikipedia.org/wiki/Flowering_plant',
        'https://en.wikipedia.org/wiki/Forage',
        'https://en.wikipedia.org/wiki/Germplasm_Resources_Information_Network',
        'https://en.wikipedia.org/wiki/Global_Biodiversity_Information_Facility',
        'https://en.wikipedia.org/wiki/Help:Category',
        'https://en.wikipedia.org/wiki/Help:Contents',
        'https://en.wikipedia.org/wiki/Help:Introduction',
        'https://en.wikipedia.org/wiki/Help:Taxon_identifiers',
        'https://en.wikipedia.org/wiki/Hybrid_(biology)',
        'https://en.wikipedia.org/wiki/INaturalist',
        'https://en.wikipedia.org/wiki/IUCN_Red_List',
        'https://en.wikipedia.org/wiki/Indigenous_people_of_the_Americas',
        'https://en.wikipedia.org/wiki/Integrated_Taxonomic_Information_System',
        'https://en.wikipedia.org/wiki/Interim_Register_of_Marine_and_Nonmarine_Genera',
        'https://en.wikipedia.org/wiki/International_Plant_Names_Index',
        'https://en.wikipedia.org/wiki/Layering',
        'https://en.wikipedia.org/wiki/Leaf',
        'https://en.wikipedia.org/wiki/Main_Page',
        'https://en.wikipedia.org/wiki/Malpighiales',
        'https://en.wikipedia.org/wiki/Marsh',
        'https://en.wikipedia.org/wiki/National_Center_for_Biotechnology_Information',
        'https://en.wikipedia.org/wiki/Natural_Resources_Conservation_Service',
        'https://en.wikipedia.org/wiki/NatureServe',
        'https://en.wikipedia.org/wiki/New_England',
        'https://en.wikipedia.org/wiki/Newfoundland_(island)',
        'https://en.wikipedia.org/wiki/Open_Tree_of_Life',
        'https://en.wikipedia.org/wiki/Plant']
    assert len(outgoing_links) == 100
