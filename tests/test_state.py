import wisconsin_covid19
import datetime
import pytest

def test_history():
    previous_date = 0
    for data in wisconsin_covid19.state.history():
        assert data.GEO == 'State'
        assert data.NAME == 'WI'
        assert data.DATE > previous_date
        previous_date = data.DATE

def test_date():
    for data in wisconsin_covid19.state.on_date(datetime.datetime.fromtimestamp(1607454559)):
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == '12/08/2020'
        assert data.GEO == 'State'
        assert data.NAME == 'WI'

# Only works if past 2pm
@pytest.mark.skip(reason="Can't ensure it's past 2pm")
def test_today():
    for data in wisconsin_covid19.state.today():
        assert datetime.datetime.fromtimestamp(data.DATE/1000).strftime('%m/%d/%Y') == datetime.datetime.now().strftime('%m/%d/%Y')
        assert data.GEO == 'State'
        assert data.NAME == 'WI'