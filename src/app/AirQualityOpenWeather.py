import pandas as pd
import requests
import app.config as config
import datetime
import time

def CallOpenWatherAirQualityCall(lon, lat, hist, startDate=0, end=0):
    response_list = []
    API_KEY = config.api_key

    if hist:
        url = config.OpenWatherAirPollutionURL_HIST
        endDate = ConvertDateTimetoUnixTime(datetime.datetime.now())
        querystring = {"lon":lon,"lat":lat, "start": startDate , "end": endDate, "appid": API_KEY}
    else:
        url = config.OpenWatherAirPollutionURL
        querystring = {"lon" : lon, "lat" : lat, "appid" : API_KEY}

    r = requests.get(url, params=querystring)
    response_list.append(r.json())

    df = pd.DataFrame.from_dict(response_list)
    return df

def Transform_AirQualityData(df, cityID):
    record_list = []
    for i in range(0, len(df['list'].to_dict()[0])):
        airquality_record = list()
        airquality_record.append(df['list'].to_dict()[0][i]['main']['aqi'])
        airquality_record.append(df['list'].to_dict()[0][i]['components']['o3'])
        airquality_record.append(df['list'].to_dict()[0][i]['components']['so2'])
        airquality_record.append(df['list'].to_dict()[0][i]['components']['no2'])
        airquality_record.append(df['list'].to_dict()[0][i]['components']['co'])
        airquality_record.append(df['list'].to_dict()[0][i]['components']['nh3'])
        airquality_record.append(df['list'].to_dict()[0][i]['components']['pm2_5'])
        airquality_record.append(df['list'].to_dict()[0][i]['components']['pm10'])
        airquality_record.append(ConvertUnixTimeToDateTime(df['list'].to_dict()[0][i]['dt']))
        airquality_record.append(cityID)
        airquality_record = tuple(airquality_record)
        record_list.append(airquality_record)
    if len(record_list) == 1:
        return airquality_record
    else:
        return record_list


def ConvertDateTimetoUnixTime(date_time):
    return int(time.mktime(date_time.timetuple()))

def ConvertUnixTimeToDateTime(unix):
    dt = datetime.datetime.fromtimestamp(unix)
    return dt



# GLAVNI ZA HISTORY
#GOTOV - UČITAVA SVE PO POZIVU (od trenutnog datuma oduzima tjedan\godinu\dvije - kako je definrano u configu do sada - trunutka pokretanja)
# Učitava podatke za svakih sat vremena 