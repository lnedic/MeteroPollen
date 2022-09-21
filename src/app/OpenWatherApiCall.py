import pandas as pd
import requests
import app.config as config
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import datetime

def CallOpenWatherApiCall(city):
    response_list = []
    API_KEY = config.api_key

    url = config.OpenWatherApiUrl
    querystring = {"q":city, "appid":API_KEY, "units":"metric"}
    r = requests.get(url, params=querystring)
    response_list.append(r.json())

    df = pd.DataFrame.from_dict(response_list)
    return df

def Transform_CityData(city, df):
    city_record = list()
    city_record.append(city)
    city_record.append(df['sys'].to_dict()[0]['country'])

    city_record.append(df['id'].to_dict()[0])
    city_record.append(city)
    city_record.append(df['coord'].to_dict()[0]['lat'])
    city_record.append(df['coord'].to_dict()[0]['lon'])
    city_record.append(df['sys'].to_dict()[0]['country'])
    city_record.append(FindTimezoneName(city))
    city_record = tuple(city_record)
    return city_record
    
def Transform_WindData(df):
    wind_record = list()
    wind_record.append(df['wind'].to_dict()[0]['speed'])
    wind_record.append('meter/sec')
    wind_record.append(GetWindDescription(df['wind'].to_dict()[0]['speed']))
    wind_record.append(df['wind'].to_dict()[0]['deg'])
    wind_record.append(GetWindDirectionCode(df['wind'].to_dict()[0]['deg']))
    wind_record.append(df['id'].to_dict()[0])
    wind_record.append(ConvertUnixTimeToDateTime(df['dt'].to_dict()[0]))
    wind_record = tuple(wind_record)
    return wind_record

def Transform_SunData(df):
    sun_record = list()
    sun_record.append(ConvertUnixTimeToDateTime(df['sys'].to_dict()[0]['sunrise']))
    sun_record.append(ConvertUnixTimeToDateTime(df['sys'].to_dict()[0]['sunset']))
    sun_record.append(df['id'].to_dict()[0])
    sun_record.append(ConvertUnixTimeToDateTime(df['dt'].to_dict()[0]))
    sun_record = tuple(sun_record)
    return sun_record

def Transform_MeteroData(df):
    metero_record = list()
    metero_record.append(df['main'].to_dict()[0]['temp'])
    metero_record.append(df['main'].to_dict()[0]['temp_min'])
    metero_record.append(df['main'].to_dict()[0]['temp_max'])
    metero_record.append(df['main'].to_dict()[0]['pressure'])
    metero_record.append(df['main'].to_dict()[0]['humidity'])
    metero_record.append(df['weather'].to_dict()[0][0]['description'])
    metero_record.append(df['visibility'].to_dict()[0])
    metero_record.append(df['clouds'].to_dict()[0]['all'])
    metero_record.append(checkPrecipitation(df))
    metero_record.append(df['id'].to_dict()[0])
    metero_record.append(ConvertUnixTimeToDateTime(df['dt'].to_dict()[0]))
    metero_record = tuple(metero_record)
    return metero_record


def Transform_PrecipitationData(df):
    multiple_rows = []
    if checkPrecipitation(df):
        precipitation_record = list()
        if 'rain' in df.columns:
            precipitation_record.append('rain')
            precipitation_record.append(df['rain'].to_dict()[0]['1h'])
            if '3h' in df['rain'].to_dict()[0]:
                precipitation_record.append(df['rain'].to_dict()[0]['3h'])
            else:
                precipitation_record.append(0.0)
            precipitation_record.append(df['id'].to_dict()[0])
            precipitation_record.append(ConvertUnixTimeToDateTime(df['dt'].to_dict()[0]))
            precipitation_record = tuple(precipitation_record)
            multiple_rows.append(precipitation_record)

        if 'snow' in df.columns:
            precipitation_record.append('snow')
            precipitation_record.append(df['snow'].to_dict()[0]['1h'])
            if '3h' in df['snow'].to_dict()[0]:
                precipitation_record.append(df['snow'].to_dict()[0]['3h'])
            else:
                precipitation_record.append(0.0)
            precipitation_record.append(df['id'].to_dict()[0])
            precipitation_record.append(ConvertUnixTimeToDateTime(df['dt'].to_dict()[0]))
            precipitation_record = tuple(precipitation_record)
            multiple_rows.append(precipitation_record)

    return multiple_rows


def FindTimezoneName(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    # getting Latitude and Longitude
    location = geolocator.geocode(city)
  
    # pass the Latitude and Longitude into a timezone_at and it return timezone
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    return result

#Beaufort scale
def GetWindDescription(speed):
    Description = ''
    if speed < 0.2 or speed == 0.2:
        Description = 'Calm'
    elif speed > 0.2 and speed < 1.5:
        Description = 'Light air'
    elif speed > 1.5 and speed < 3.3:
        Description = 'Light breeze'
    elif speed > 3.3 and speed < 5.5:
        Description = 'Gentle breeze'
    elif speed > 5.5 and speed < 7.9:
        Description = 'Moderate breeze'
    elif speed > 7.9 and speed < 10.7:
        Description = 'Fresh breeze'
    elif speed > 10.7 and speed < 13.8:
        Description = 'Strong breeze'
    elif speed > 13.8 and speed < 17.1:
        Description = 'High wind, moderate gale, near gale'
    elif speed >17.1 and speed < 20.7:
        Description = 'Gale, fresh gale'
    elif speed > 20.7 and speed < 24.4:
        Description = 'Strong/severe gale'
    elif speed > 24.4 and speed < 28.4:
        Description = 'Storm, whole gale'
    elif speed > 28.4 and speed < 32.6:
        Description = 'Violent storm'
    elif speed > 32.6:
        Description = 'Hurricane force'

    return Description


def GetWindDirectionCode(direction):
    if direction > 348.75  or direction < 11.25:
        Code = 'N';
    elif direction > 11.25 and direction < 33.75:
        Code = 'NNE';
    elif direction > 33.75 and direction < 56.25:
        Code = 'NE';
    elif direction > 56.25 and direction < 78.75:
        Code = 'ENE';
    elif direction > 78.75 and direction < 101.25:
        Code = 'E';
    elif direction > 101.25 and direction < 123.75:
        Code = 'ESE';
    elif direction > 123.75 and direction < 146.25:
        Code = 'SE';
    elif direction > 146.25 and direction < 168.75:
        Code = 'SSE';
    elif direction > 168.75 and direction < 191.25:
        Code = 'S';
    elif direction > 191.25 and direction < 213.75:
        Code = 'SSW';
    elif direction > 213.75 and direction < 236.25:
        Code = 'SW';
    elif direction > 236.25 and direction < 258.75:
        Code = 'WSW';
    elif direction > 258.75 and direction < 281.25:
        Code = 'W';
    elif direction > 281.25 and direction < 303.75:
        Code = 'WNW';
    elif direction > 303.75 and direction < 326.25:
        Code = 'NW';
    elif direction > 326.25 and direction < 348.75:
        Code = 'NNW';
    return Code;

def ConvertUnixTimeToDateTime(unix):
    dt = datetime.datetime.fromtimestamp(unix)
    return dt


def checkPrecipitation(df):
    precipitation = False
    if 'rain' in df.columns or 'snow' in df.columns:
        precipitation = True
    return precipitation


def GetCityData(city):
    response_list = []
    API_KEY = config.api_key

    url = config.OpenWatherApiUrl
    querystring = {"q":city, "appid":API_KEY, "units":"metric"}
    r = requests.get(url, params=querystring)
    response_list.append(r.json())
    df = pd.DataFrame.from_dict(response_list)

    #country = df['sys'].to_dict()[0]['country']
    #cityID = df['id'].to_dict()[0]
    dict = {"id":df['id'].to_dict()[0], "name" : city, "country" : df['sys'].to_dict()[0]['country']}
    return dict

# GLAVNI POZIV ZA TRENUTNO VRIJEME -> GOTOVO