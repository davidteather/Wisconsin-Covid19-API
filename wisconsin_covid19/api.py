import requests
import datetime
import logging
from urllib.parse import urlencode

from .models import CovidData
from .exceptions import InvalidAPIResponse

#
# Common Methods
#
def get_data(query, server_id, ordering="ASC", custom_base="https://dhsgis.wi.gov/server/rest/services/DHS_COVID19/COVID19_WI/MapServer/", **kwargs):
    query = {
        'where': query,
        'outFields': '*',
        'orderByFields': 'DATE {}'.format(ordering),
        'outSR': 4326,
        'f': 'json'
    }
    query.update(kwargs.get('api_params', {}))

    api_url = custom_base + "{}/query?{}".format(server_id, urlencode(query))
    r = requests.get(api_url)
    formatted_json = r.json()

    if "error" in formatted_json.keys():
        logging.error(api_url)
        logging.error(formatted_json)
        raise InvalidAPIResponse()

    if len(formatted_json.get('features', [])) == 0:
        logging.error(api_url)
        logging.error(query)
        raise InvalidAPIResponse(message="No COVID data returned from api, query may be wrong. If you're using a on_date function the data may not have been released for that day yet. Data is released at 2pm Central Time.")

    for data_point in formatted_json['features']:
        yield CovidData(data_point['attributes'])

def datetime_to_timestamp(date, hour_time):
    return date.strftime("%Y-%m-%d ") + hour_time

def datetime_to_query(date):
    return "DATE >= TIMESTAMP '{}' AND DATE <= '{}'".format(datetime_to_timestamp(date, "00:00:00"), datetime_to_timestamp(date, "23:59:59"))

#
# Testing Site API Requests
#
# server_id=0
#
class testing_site:
    testing_api = "https://dhsgis.wi.gov/server/rest/services/DHS_COVID19/COVID19_Community_Testing_Sites/MapServer/"
    @staticmethod
    def all(**kwargs):
        return get_data("1=1", server_id=0, custom_base=testing_site.testing_api, api_params={'orderByFields': ''}, **kwargs)

    @staticmethod
    def city_search(city_name, **kwargs):
        return get_data("CITY = '{}'".format(city_name), server_id=0, custom_base=testing_site.testing_api, api_params={'orderByFields': ''},**kwargs)

    @staticmethod
    def county_search(county_name, **kwargs):
        return get_data("COUNTY = '{}'".format(county_name), server_id=0, custom_base=testing_site.testing_api, api_params={'orderByFields': ''},**kwargs)

    @staticmethod
    def zipcode_search(zip_code, **kwargs):
        return get_data("ZIP = '{}'".format(zip_code), server_id=0, custom_base=testing_site.testing_api, api_params={'orderByFields': ''}, **kwargs)

#
# Wisconsin State API Requests
# 
# server_id=11
#
class state:
    @staticmethod
    def history(**kwargs):
        return get_data("GEO='State'", server_id=11, **kwargs) 

    @staticmethod
    def on_date(date, **kwargs):
        return get_data("GEO='State' AND {}".format(datetime_to_query(date)), server_id=11, **kwargs) 

    @staticmethod
    def today(**kwargs):
        return state.on_date(datetime.datetime.now(), **kwargs)

#
# County Data
#
# server_id=12
# Example county_name="Adams" not "Adams County"
#
class county:
    @staticmethod
    def history(county_name, **kwargs):
        return get_data("GEO='County' AND NAME = '{}'".format(county_name), server_id=12, **kwargs) 
    
    @staticmethod
    def history_all(**kwargs):
        return get_data("GEO='County'", server_id=12, **kwargs) 

    @staticmethod
    def on_date(county_name, date, **kwargs):
        return get_data("GEO='County' AND NAME = '{}' AND {}".format(county_name, datetime_to_query(date)), server_id=12, **kwargs) 

    @staticmethod
    def on_date_all(date, **kwargs):
        return get_data("GEO='County' AND {}".format(datetime_to_query(date)), server_id=12, **kwargs) 

    @staticmethod
    def today(county_name, **kwargs):
        return county.on_date(county_name, datetime.datetime.now(), **kwargs)

    @staticmethod
    def today_all(**kwargs):
        return county.on_date_all(datetime.datetime.now(), **kwargs)


#
# Census Tracts API Requests
#
# server_id=13 is the census tract data
#
class census_tract:
    @staticmethod
    def history(tract_id, **kwargs):
        return get_data("GEO='Census tract' AND GEOID = '{}'".format(tract_id), server_id=13, **kwargs) 

    @staticmethod
    def history_all(**kwargs):
        return get_data("GEO='Census tract'", server_id=13, **kwargs) 

    @staticmethod
    def on_date(tract_id, date, **kwargs):
        return get_data("GEO='Census tract' AND GEOID = '{}' AND {}".format(tract_id, datetime_to_query(date)), server_id=13, **kwargs) 

    @staticmethod
    def on_date_all(date, **kwargs):
        return get_data("GEO='Census tract' AND {}".format(datetime_to_query(date)), server_id=13, **kwargs) 

    @staticmethod
    def today(tract_id, **kwargs):
        return census_tract.on_date(tract_id, datetime.datetime.now(), **kwargs)

    @staticmethod
    def today_all(**kwargs):
        return census_tract.on_date_all(datetime.datetime.now(), **kwargs)

#
# School District API Requests
#
# server_id=14
#
class school_district:
    @staticmethod
    def history(school_district, **kwargs):
        return get_data("GEO='School district' AND NAME = '{}'".format(school_district), server_id=14, **kwargs) 

    @staticmethod
    def history_all(**kwargs):
        return get_data("GEO='School district'", server_id=14, **kwargs) 

    @staticmethod
    def on_date(school_district, date, **kwargs):
        return get_data("GEO='School district' AND NAME = '{}' AND {}".format(school_district, datetime_to_query(date)), server_id=14, **kwargs) 

    @staticmethod
    def on_date_all(date, **kwargs):
        return get_data("GEO='School district' AND {}".format(datetime_to_query(date)), server_id=14, **kwargs) 

    @staticmethod
    def today(school_district, **kwargs):
        return school_district.on_date(school_district, datetime.datetime.now(), **kwargs)

    @staticmethod
    def today_all(**kwargs):
        return school_district.on_date_all(datetime.datetime.now(), **kwargs)

#
# City/Village/Town API Requests
#
# server_id=16
#
class city:
    @staticmethod
    def history(city_name, city_type, **kwargs):
        return get_data("GEO='County subdivision' AND NAME = '{} {}'".format(city_name, city_type), server_id=16, **kwargs) 

    @staticmethod
    def history_all_city_types(city_name, **kwargs):
        return get_data("GEO='County subdivision' AND (NAME = '{} city' OR NAME = '{} village' OR NAME = '{} town') ".format(city_name, city_name, city_name), server_id=16, **kwargs) 

    @staticmethod
    def history_all(**kwargs):
        return get_data("GEO='County subdivision'", server_id=16, **kwargs) 

    @staticmethod
    def on_date(city_name, city_type, date, **kwargs):
        return get_data("GEO='County subdivision' AND NAME = '{} {}' AND {}".format(city_name, city_type, datetime_to_query(date)), server_id=16, **kwargs) 

    @staticmethod
    def on_date_all_city_types(city_name, date, **kwargs):
        return get_data("GEO='County subdivision' AND (NAME = '{} city' OR NAME = '{} village' OR NAME = '{} town') AND {}".format(city_name, city_name, city_name, datetime_to_query(date)), server_id=16, **kwargs) 

    @staticmethod
    def on_date_all(date, **kwargs):
        return get_data("GEO='County subdivision' AND {}".format(datetime_to_query(date)), server_id=16, **kwargs) 

    @staticmethod
    def today(city_name, city_type, **kwargs):
        return city.on_date(city_name, city_type, datetime.datetime.now(), **kwargs)

    @staticmethod
    def today_all(**kwargs):
        return city.on_date_all(datetime.datetime.now(), **kwargs)
#
# ZIP Code API Requests
#
# server_id=17
#
class zip_code:
    @staticmethod
    def history(zip_code, **kwargs):
        return get_data("GEO='ZCTA' AND NAME = '{}'".format(zip_code), server_id=17, **kwargs) 

    @staticmethod
    def history_all(**kwargs):
        return get_data("GEO='ZCTA'", server_id=17, **kwargs) 

    @staticmethod
    def on_date(zip_code, date, **kwargs):
        return get_data("GEO='ZCTA' AND NAME = '{}' AND {}".format(zip_code, datetime_to_query(date)), server_id=17, **kwargs) 

    @staticmethod
    def on_date_all(date, **kwargs):
        return get_data("GEO='ZCTA' AND {}".format(datetime_to_query(date)), server_id=17, **kwargs) 

    @staticmethod
    def today(zip_code, **kwargs):
        return zip_code.on_date(zip_code, datetime.datetime.now(), **kwargs)

    @staticmethod
    def today_all(**kwargs):
        return zip_code.on_date_all(datetime.datetime.now(), **kwargs)

#
# Misc
#
def custom_query(query, server_id, **kwargs):
    return get_data(query, server_id, **kwargs)