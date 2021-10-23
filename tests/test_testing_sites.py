import wisconsin_covid19
def test_all():
    count = 0
    for site in wisconsin_covid19.testing_site.all():
        # There's 3 MN for some reason
        assert 'WI' in site.STATE or site.STATE == "MN"
        count += 1

    assert count > 0

def test_city_search():
    for site in wisconsin_covid19.testing_site.city_search('Madison'):
        assert 'WI' in site.STATE
        assert site.CITY == 'Madison'

def test_county_search():
    for site in wisconsin_covid19.testing_site.county_search('Dane'):
        assert 'WI' in site.STATE
        assert site.COUNTY.replace(" ", "") == 'Dane'

def test_zipcode_search():
    for site in wisconsin_covid19.testing_site.zipcode_search(53703):
        assert 'WI' in site.STATE
        assert site.COUNTY.replace(" ", "") == 'Dane'
        assert site.ZIP == 53703
