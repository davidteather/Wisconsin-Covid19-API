import wisconsin_covid19
import datetime
import pytest

def test_history():
    previous_date = 0
    for data in wisconsin_covid19.zip_code.history('53558'):
        assert data.GEO == 'ZCTA'
        assert data.NAME == '53558'
        assert data.DATE > previous_date
        previous_date = data.DATE

def test_history_all():
    previous_date = 0
    for data in wisconsin_covid19.zip_code.history_all():
        assert data.GEO == 'ZCTA'
        assert data.DATE >= previous_date
        previous_date = data.DATE

def test_date():
    for data in wisconsin_covid19.zip_code.on_date('53558', datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.NAME == '53558'
        assert data.GEO == 'ZCTA'

def test_date_all():
    previous_date = 0
    for data in wisconsin_covid19.zip_code.on_date_all(datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.GEO == 'ZCTA'
        assert data.DATE >= previous_date
        previous_date = data.DATE

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today():
    for data in wisconsin_covid19.zip_code.today('53558'):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.NAME == '53558'
        assert data.GEO == 'ZCTA'

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today_all():
    for data in wisconsin_covid19.zip_code.today_all():
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.GEO == 'ZCTA'