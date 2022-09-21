api_key = '35ea9499bd1265c0056d68a687a98d65'
WU_api_key = '958ff199cfe64f188ff199cfe61f189c'

#auth data for meteomatics
user_metero = '-_nedic'
password_metero = '0HJlSWq57j'

#urls for api
OpenWatherApiUrl = 'https://api.openweathermap.org/data/2.5/weather'
AirQualityApiUrl = "https://air-quality.p.rapidapi.com/current/airquality"
OpenWatherAirPollutionURL = "http://api.openweathermap.org/data/2.5/air_pollution"

#History URLS
AirQualityApiUrl_HIST = "https://air-quality.p.rapidapi.com/history/airquality"
OpenWatherHistoryApiUrl = "http://api.openweathermap.org/data/3.0/onecall/timemachine"
OpenWatherAirPollutionURL_HIST = "http://api.openweathermap.org/data/2.5/air_pollution/history"

#PostgreSQL database data
database = 'postgres'
database_user = 'postgres'
database_password= 'admin'
database_host = 'localhost'
database_port = '5432'
database_newDatabaseName = 'meteropollen_db'

#token for 
token = '2caa435e4eeaf2a373504f269482875cf93b5eac'

#Header data for AirQulityApi
X_RapidAPI_Key = "45890264e1msh908d45da5462129p195224jsne758b9056578"
X_RapidAPI_Host = "air-quality.p.rapidapi.com"

#SQL insert queries
SQL_QUERIES = {}
#SQL_QUERIES['City'] = """ INSERT INTO City (CityName, lat, lon, Country, Timezone) VALUES (%s,%s, %s, %s, %s) """
SQL_QUERIES['Wind'] = """ INSERT INTO Wind (Speed, SpeedUnit, Description, Direction, Code, CityID, DateTime) VALUES %s """
SQL_QUERIES['Sun'] = """ INSERT INTO Sun (Sunrise, Sunset, CityID, DateTime) VALUES %s """
SQL_QUERIES['Precipitation'] = """ INSERT INTO Precipitation (Description, vol_1h, vol_3h, CityID, DateTime) VALUES %s"""
SQL_QUERIES['MeteorologicalData'] = """ INSERT INTO MeteorologicalData (Temperature,Temp_min,Temp_max,Presure,Humidity,Description,visibility,Cloudly,Precipitation,CityID,DateTime) VALUES %s """
SQL_QUERIES['AirQuality'] = """ INSERT INTO AirQuality (aqi,o3,so2,no2,co,nh3,pm25,pm10,DateTime, CityID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
SQL_QUERIES['City'] = """ DO $$
                            BEGIN 
                            IF NOT EXISTS(Select * from City where cityname=%s and country=%s) THEN
                                    INSERT INTO City (CityID, CityName, lat, lon, Country, Timezone) VALUES (%s, %s, %s, %s, %s, %s); 
                            END IF;
                          END $$; """

SQL_QUERIES['All'] = """ DO $$
                            BEGIN 
                            IF NOT EXISTS(Select * from City where cityname=%s and country=%s) THEN
                                    INSERT INTO City (CityID, CityName, lat, lon, Country, Timezone) VALUES (%s, %s, %s, %s, %s, %s); 
                            END IF;
                         END $$;
                          
                         INSERT INTO Wind (Speed, SpeedUnit, Description, Direction, Code, CityID, DateTime) VALUES (%s,%s, %s, %s, %s, %s,%s);
                         INSERT INTO Sun (Sunrise, Sunset, CityID, DateTime) VALUES (%s,%s, %s, %s) ;
                         INSERT INTO MeteorologicalData (Temperature,Temp_min,Temp_max,Presure,Humidity,Description,visibility,Cloudly,Precipitation,CityID,DateTime) VALUES (%s,%s, %s, %s, %s,%s,%s,%s, %s, %s, %s);
                         INSERT INTO AirQuality (aqi,o3,so2,no2,co,nh3,pm25,pm10, DateTime, CityID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                     """

SQL_QUERIES['History All'] = """
                         INSERT INTO Wind (Speed, SpeedUnit, Description, Direction, Code, CityID, DateTime) VALUES (%s,%s, %s, %s, %s, %s,%s);
                         INSERT INTO Sun (Sunrise, Sunset, CityID, DateTime) VALUES (%s,%s, %s, %s) ;
                         INSERT INTO MeteorologicalData (Temperature,Presure,Humidity,Description,visibility,Cloudly,Precipitation,CityID,DateTime) VALUES (%s,%s, %s, %s, %s,%s,%s,%s, %s);
                        """
SQL_QUERIES['History Precipitation'] = """ INSERT INTO Precipitation (Description, vol_1h, CityID, DateTime) VALUES %s"""

TABLES = ['City', 'Wind', 'Sun', 'MeteorologicalData', 'AirQuality', 'Precipitation']
years_diff = 0.5


city_for_sync = ['Zagreb', 'Novi Sad', 'Osijek', 'Beograd', 'Split', 'Dubrovnik', 'Slavonski Brod']