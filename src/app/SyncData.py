import psycopg2
import app.config as config
from psycopg2.extras import execute_values
from OpenWatherApiCall import CallOpenWatherApiCall, Transform_CityData, Transform_WindData, Transform_SunData, Transform_MeteroData, Transform_PrecipitationData
#from AirQualityApiCall import CallAirQualityApi, Transform_AirQualityData
from app.AirQualityOpenWeather import CallOpenWatherAirQualityCall, Transform_AirQualityData


def insert_SyncData(tableName, data, precipitationData):
    try:
        connection = psycopg2.connect(database=config.database_newDatabaseName, 
                        user=config.database_user, 
                        password=config.database_password, 
                        host=config.database_host, 
                        port= config.database_port)

        cursor = connection.cursor()
        #define sql query to execute from config
        sql_insert_query = config.SQL_QUERIES[tableName]
        
        #insert data to all table except in Precipitation
        cursor.execute(sql_insert_query, data)

        #insert line/lines in Precipitation if exists
        if len(precipitationData) > 0:
            sql_insert_query = config.SQL_QUERIES['Precipitation']
            execute_values(cursor, sql_insert_query, precipitationData)

        connection.commit()
        #print(cursor.rowcount, "Record inserted successfully into {} table".format(tableName))
        print(':  Succes')
    except (Exception, psycopg2.Error) as error:
        print(':  Failed', end =" ")
        print("Failed inserting record into {} table {}".format(tableName,error))

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")



def SyncData(city):
    #Call Api
    df = CallOpenWatherApiCall(city)
    
    #if Api don't response properly
    if df['cod'].to_dict()[0] != 200:
        print('Something wrong happend, check parameters and try again')
        if 'message' in df.columns:
            print('Api error message: ', df['message'].to_dict()[0])
        return 
   
    #if Api response correctly        
    CityData = Transform_CityData(city, df)
    #print(CityData)
#------------------------------------------------------------------------------------------------------------------
    #Call Air Quality Api after the city data was transformed with City coordinate lon, lat
    #dfAirQuality = CallAirQualityApi(CityData[5], CityData[4], False)
    #AirQualityData = Transform_AirQualityData(dfAirQuality)
    #AirQualityData += tuple([CityData[2], WindData[-1]])
    #print(AirQualityData)
#------------------------------------------------------------------------------------------------------------------
     #AirQuality Api Call 
    AirQulatiydf = CallOpenWatherAirQualityCall(CityData[5],CityData[4], False)
    AirQualityData = Transform_AirQualityData(AirQulatiydf, CityData[2])
    #print(AirQualityData)

    WindData = Transform_WindData(df)
    #print(WindData)

    SunData = Transform_SunData(df)
    #print(SunData)

    MeteroData = Transform_MeteroData(df)
    #print(MeteroData)

    PrecipitationData = Transform_PrecipitationData(df)
    #print(PrecipitationData)

    insert_SyncData('All', CityData + WindData + SunData + MeteroData + AirQualityData, PrecipitationData)



