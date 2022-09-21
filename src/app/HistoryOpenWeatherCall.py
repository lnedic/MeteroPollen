import pandas as pd
import requests
import app.config as config
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import time
from OpenWatherApiCall import GetWindDescription, GetWindDirectionCode, ConvertUnixTimeToDateTime, GetCityData


def CallOpenWatherApiCall(city, date):
    response_list = []
    API_KEY = config.api_key
    url = config.OpenWatherHistoryApiUrl
    lon, lat = FindTimezoneName(city)
    query_string = {"lat" : lat, "lon": lon, "dt": date, "appid": API_KEY, "units": 'metric'}
    r = requests.get(url, params=query_string)
    response_list.append(r.json())
    
     #city data
    response_list[0]['city'] = GetCityData(city)
    df = pd.DataFrame.from_dict(response_list)
    return df

def FindTimezoneName(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city)
    return (location.longitude, location.latitude)


def Transform_CityData(city, df):
    city_record = list()
    city_record.append(city)
    city_record.append(df['city'].to_dict()[0]['country'])

    city_record.append(df['city'].to_dict()[0]['id'])
    city_record.append(city)
    city_record.append(df['lat'].to_dict()[0])
    city_record.append(df['lon'].to_dict()[0])
    city_record.append(df['city'].to_dict()[0]['country'])
    city_record.append(df['timezone'].to_dict()[0])
    city_record = tuple(city_record)
    return city_record

def Transform_WindData(df):
    wind_record = list()
    wind_record.append(df['data'].to_dict()[0][0]['wind_speed'])
    wind_record.append('meter/sec')
    wind_record.append(GetWindDescription(df['data'].to_dict()[0][0]['wind_speed']))
    wind_record.append(df['data'].to_dict()[0][0]['wind_deg'])
    wind_record.append(GetWindDirectionCode(df['data'].to_dict()[0][0]['wind_deg']))
    wind_record.append(df['city'].to_dict()[0]['id'])
    wind_record.append(ConvertUnixTimeToDateTime(df['data'].to_dict()[0][0]['dt']))
    wind_record = tuple(wind_record)
    return wind_record

def Transform_SunData(df):
    sun_record = list()
    sun_record.append(ConvertUnixTimeToDateTime(df['data'].to_dict()[0][0]['sunrise']))
    sun_record.append(ConvertUnixTimeToDateTime(df['data'].to_dict()[0][0]['sunset']))
    sun_record.append(df['city'].to_dict()[0]['id'])
    sun_record.append(ConvertUnixTimeToDateTime(df['data'].to_dict()[0][0]['dt']))
    sun_record = tuple(sun_record)
    return sun_record

def Transform_MeteroData(df):
    metero_record = list()
    metero_record.append(df['data'].to_dict()[0][0]['temp'])
    #metero_record.append(df['data'].to_dict()[0]['temp_min'])
    #metero_record.append(df['data'].to_dict()[0]['temp_max'])
    metero_record.append(df['data'].to_dict()[0][0]['pressure'])
    metero_record.append(df['data'].to_dict()[0][0]['humidity'])
    metero_record.append(df['data'].to_dict()[0][0]['weather'][0]['description'])
    if 'visibility' in df['data'].to_dict()[0][0]:
        metero_record.append(df['data'].to_dict()[0][0]['visibility'])
    else:
        metero_record.append(-1)
    metero_record.append(df['data'].to_dict()[0][0]['clouds'])
    metero_record.append(checkPrecipitation(df['data'][0][0]))
    metero_record.append(df['city'].to_dict()[0]['id'])
    metero_record.append(ConvertUnixTimeToDateTime(df['data'].to_dict()[0][0]['dt']))
    metero_record = tuple(metero_record)
    return metero_record

def Transform_PrecipitationData(df):
    multiple_rows = []
    if checkPrecipitation(df['data'][0][0]):
        precipitation_record = list()
        if 'rain' in df['data'][0][0]:
            precipitation_record.append('rain')
            if '1h' in df['data'][0][0]['rain']:
                precipitation_record.append(df['data'][0][0]['rain']['1h'])
            elif '3h' in df['data'][0][0]['rain']:
                precipitation_record.append(df['data'][0][0]['rain']['3h'])
            else:
                precipitation_record.append(df['data'][0][0]['rain'])
            
            precipitation_record.append(df['city'].to_dict()[0]['id'])
            precipitation_record.append(ConvertUnixTimeToDateTime(df['data'].to_dict()[0][0]['dt']))
            precipitation_record = tuple(precipitation_record)
            multiple_rows.append(precipitation_record)

        if 'snow' in df['data'][0][0]:
            precipitation_record.append('snow')
            if '1h' in df['data'][0][0]['snow']:
                precipitation_record.append(df['data'][0][0]['snow']['1h'])
            elif '3h' in df['data'][0][0]['snow']:
                precipitation_record.append(df['data'][0][0]['snow']['3h'])
            else:
                precipitation_record.append(df['data'][0][0]['snow'])
    
            precipitation_record.append(df['city'].to_dict()[0]['id'])
            precipitation_record.append(ConvertUnixTimeToDateTime(df['data'].to_dict()[0][0]['dt']))
            precipitation_record = tuple(precipitation_record)
            multiple_rows.append(precipitation_record)

    return multiple_rows


def ConvertDateTimetoUnixTime(date_time):
    return int(time.mktime(date_time.timetuple()))

def checkPrecipitation(df):
    precipitation = False
    if 'rain' in df or 'snow' in df:
        precipitation = True
    return precipitation



#df = CallOpenWatherApiCall('Zagreb', StartDate)
#print(df)
"""
city_data = Transform_CityData('Zagreb', df)
print(city_data)
sun_data = Transform_SunData(df)
print(sun_data)
wind_data = Transform_WindData(df)
print(wind_data)
metero_data = Transform_MeteroData(df)
print(metero_data)
precipitation_data = Transform_PrecipitationData(df)
print(precipitation_data)
"""