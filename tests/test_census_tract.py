import wisconsin_covid19
import datetime
import pytest

#
# Census Tract
#
# find number on https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx get rid of decimal by *100
# find the FIPS of the county https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697
# concatenate FIPS + census_tract
#

def test_history():
    previous_date = 0
    for data in wisconsin_covid19.census_tract.history('55025' + '001705'):
        assert data.GEO == 'Census tract'
        assert data.GEOID == '55025' + '001705'
        assert data.DATE > previous_date
        previous_date = data.DATE

def test_history_all():
    previous_date = 0
    for data in wisconsin_covid19.census_tract.history_all():
        assert data.GEO == 'Census tract'
        assert data.DATE >= previous_date
        previous_date = data.DATE

def test_date():
    for data in wisconsin_covid19.census_tract.on_date('55025' + '001705', datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.GEOID == '55025' + '001705'
        assert data.GEO == 'Census tract'

def test_date_all():
    previous_date = 0
    for data in wisconsin_covid19.census_tract.on_date_all(datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.GEO == 'Census tract'
        assert data.DATE >= previous_date
        previous_date = data.DATE

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today():
    for data in wisconsin_covid19.census_tract.today('55025' + '001705'):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.GEOID == '55025' + '001705'
        assert data.GEO == 'Census tract'

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today_all():
    for data in wisconsin_covid19.census_tract.today_all():
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.GEO == 'Census tract'