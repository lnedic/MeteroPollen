import pandas as pd
import requests
import app.config as config
import datetime
import time

def CallWatherUndergroudAPI():
    response_list = []
    url = 'https://api.weather.com/v2/pws/history/daily?apiKey={}'.format(config.WU_api_key)
    endDate = '20201001'
    querystring = {"stationId":'IOSIJE10',"format":'json', "units":'m' , "date": endDate}

    r = requests.get(url, params=querystring)
    response_list.append(r.json())

    df = pd.DataFrame.from_dict(response_list)
    return df


def Transform_WUData(df):
    record_list = []
    record = list()
    record.append(df['observations'].to_dict()[0][0]['stationID'])
    record.append(df['observations'].to_dict()[0][0]['tz'])
    record.append(df['observations'].to_dict()[0][0]['obsTimeLocal'])
    record.append(df['observations'].to_dict()[0][0]['lat'])
    record.append(df['observations'].to_dict()[0][0]['lon'])
    record.append(df['observations'].to_dict()[0][0]['winddirAvg'])

    record = tuple(record)
    record_list.append(record)
    print(record)
    return record_list

df = CallWatherUndergroudAPI()
data = Transform_WUData(df)
print(data)


