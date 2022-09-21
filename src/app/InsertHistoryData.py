import app.config as config
import psycopg2
import time
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
from app.HistoryOpenWeatherCall import CallOpenWatherApiCall, Transform_CityData, Transform_SunData, Transform_MeteroData, Transform_WindData, Transform_PrecipitationData
from AirQualityOpenWeather import CallOpenWatherAirQualityCall, Transform_AirQualityData

def insert_HistoryData(tableName,CityData, data, precipitationData, AirQualityData):
    try:
        connection = psycopg2.connect(database=config.database_newDatabaseName, 
                        user=config.database_user, 
                        password=config.database_password, 
                        host=config.database_host, 
                        port= config.database_port)

        cursor = connection.cursor()
        sql_cityInsert = config.SQL_QUERIES['City']
        result = cursor.executemany(sql_cityInsert, CityData)

        #insert line/lines in Precipitation if exists
        for i in range(len(precipitationData)):
            if len(precipitationData[i]) > 0:
                sql_insert_query = config.SQL_QUERIES['History Precipitation']
                execute_values(cursor, sql_insert_query, precipitationData[i])

        #insert all other data 
        sql_insert_query = config.SQL_QUERIES[tableName]
        result = cursor.executemany(sql_insert_query, data)

        #insert airQuality Data
        sql_insert_query = config.SQL_QUERIES['AirQuality']
        result = cursor.executemany(sql_insert_query, AirQualityData)

        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into {} table".format(tableName))

    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into {} table {}".format(tableName,error))

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")




def HistoryDataReload(city, currentDate):
    #Call Api
    df = CallOpenWatherApiCall(city, currentDate)

    #if Api don't response properly
    if 'cod' in df.columns and df['cod'].to_dict()[0] != 200:
        print('Something wrong happend, check parameters and try again')
        if 'message' in df.columns:
            print('Api error message: ', df['message'].to_dict()[0])
        return
   
    #if Api response correctly        
    CityData = Transform_CityData(city, df)
    #print(CityData)

    WindData = Transform_WindData(df)
    #print(WindData)

    SunData = Transform_SunData(df)
    #print(SunData)

    MeteroData = Transform_MeteroData(df)
    #print(MeteroData)

    PrecipitationData = Transform_PrecipitationData(df)
    #print(PrecipitationData)

    return (CityData, (WindData + SunData + MeteroData), PrecipitationData)


def ConvertDateTimetoUnixTime(date_time):
    return int(time.mktime(date_time.timetuple()))

def ConvertUnixTimeToDateTime(unix):
    dt =datetime.fromtimestamp(unix)
    return dt

def CalculateStartDate():
    today = datetime.now()
    delta = timedelta(days=366*config.years_diff)
    #delta = timedelta(weeks=2)
    date = today - delta
    print("Start date in database: ", date) 
    return ConvertDateTimetoUnixTime(date)

def CalculateNextDate(currentDate):
    delta = timedelta(seconds=86400)
    date = currentDate + delta
    return date


def LoadHistoryInDatabase(cityName):
    city = []
    Data = []
    Precipitation = []

    StartDateUnix = CalculateStartDate()
    StartDate = ConvertUnixTimeToDateTime(StartDateUnix)
    #print(StartDate)
    CurrDate = StartDate
    while  CurrDate.date() != datetime.now().date():
        CurrDate = ConvertDateTimetoUnixTime(CurrDate)
        currCity, currData, currPrecipitation = HistoryDataReload(cityName, CurrDate)
        city.append(currCity)
        Data.append(currData)
        Precipitation.append(currPrecipitation)
        CurrDate = CalculateNextDate(ConvertUnixTimeToDateTime(CurrDate))

    #AirQuality Api Call (every hour)
    AirQulatiydf = CallOpenWatherAirQualityCall(city[0][5],city[0][4], True, StartDateUnix)
    AirQuality = Transform_AirQualityData(AirQulatiydf, city[0][2])

    print(city)
    print(Data)
    print(Precipitation)
    insert_HistoryData('History All', city, Data, Precipitation, AirQuality)




#Get History data and load them in database
#LoadHistoryInDatabase()
