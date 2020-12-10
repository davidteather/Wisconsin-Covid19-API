import wisconsin_covid19
import datetime
import pytest

def test_history():
    previous_date = 0
    for data in wisconsin_covid19.city.history('Blanchard', 'town'):
        assert data.GEO == 'County subdivision'
        assert data.NAME == 'Blanchard town'
        assert data.DATE > previous_date
        previous_date = data.DATE

def test_history_all_city_types():
    previous_date = 0
    for data in wisconsin_covid19.city.history_all_city_types('Blanchard'):
        assert data.GEO == 'County subdivision'
        assert 'Blanchard' in data.NAME
        assert data.DATE > previous_date
        previous_date = data.DATE

def test_history_all():
    previous_date = 0
    for data in wisconsin_covid19.city.history_all():
        assert data.GEO == 'County subdivision'
        assert data.DATE >= previous_date
        previous_date = data.DATE

def test_date():
    for data in wisconsin_covid19.city.on_date('Blanchard', 'town', datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.NAME == 'Blanchard town'
        assert data.GEO == 'County subdivision'

def test_date_all_city_types():
    for data in wisconsin_covid19.city.on_date_all_city_types('Blanchard', datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert 'Blanchard' in data.NAME
        assert data.GEO == 'County subdivision'

def test_date_all():
    previous_date = 0
    for data in wisconsin_covid19.city.on_date_all(datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.GEO == 'County subdivision'
        assert data.DATE >= previous_date
        previous_date = data.DATE

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today():
    for data in wisconsin_covid19.city.today('Blanchard', 'town'):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.NAME == 'Blanchard town'
        assert data.GEO == 'County subdivision'

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today_all():
    for data in wisconsin_covid19.city.today_all():
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.GEO == 'County subdivision'