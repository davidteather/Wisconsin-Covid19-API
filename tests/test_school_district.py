import wisconsin_covid19
import datetime
import pytest

def test_history():
    previous_date = 0
    for data in wisconsin_covid19.school_district.history('Clayton'):
        assert data.GEO == 'School district'
        assert data.NAME == 'Clayton'
        assert data.DATE > previous_date
        previous_date = data.DATE

def test_history_all():
    previous_date = 0
    for data in wisconsin_covid19.school_district.history_all():
        assert data.GEO == 'School district'
        assert data.DATE >= previous_date
        previous_date = data.DATE

def test_date():
    for data in wisconsin_covid19.school_district.on_date('Clayton', datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.NAME == 'Clayton'
        assert data.GEO == 'School district'

def test_date_all():
    previous_date = 0
    for data in wisconsin_covid19.school_district.on_date_all(datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.GEO == 'School district'
        assert data.DATE >= previous_date
        previous_date = data.DATE

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today():
    for data in wisconsin_covid19.school_district.today('Clayton'):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.NAME == 'Clayton'
        assert data.GEO == 'School district'

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today_all():
    for data in wisconsin_covid19.school_district.today_all():
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.GEO == 'School district'