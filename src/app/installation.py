import psycopg2
import app.config as config

#establishing the connection
conn = psycopg2.connect(database=config.database, 
                        user=config.database_user, 
                        password=config.database_password, 
                        host=config.database_host, 
                        port= config.database_port)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = '''CREATE database ''' + config.database_newDatabaseName + '';

#Creating a database
cursor.execute(sql)
print("Database created successfully........")
#Close current connection 
conn.close()

#Connect to new database
conn = psycopg2.connect(database=config.database_newDatabaseName, 
                        user=config.database_user, 
                        password=config.database_password, 
                        host=config.database_host, 
                        port= config.database_port)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Create tables in Database
sqlCreate = """
            CREATE TABLE City (
                CityID int PRIMARY KEY,
                CityName varchar(255) NOT NULL,
                lat float NOT NULL,
                lon float4 NOT NULL,
                Country varchar(255),
                Timezone varchar(255)
            );
            """ 

cursor.execute(sqlCreate)
print("Table City created successfully........")
#############################################################
sqlCreate = """
            CREATE TABLE Wind (
                WindID SERIAL NOT NULL,
                Speed float NOT NULL,
                SpeedUnit VARCHAR(20),
                Description VARCHAR(255),
                Direction float NOT NULL,
                Code varchar(10),
                CityID int,
                DateTime timestamptz NOT NULL,
                PRIMARY KEY (WindID, DateTime),
				CONSTRAINT fk_city
				  FOREIGN KEY(CityID) 
				  REFERENCES City(CityID)
            );
            """ 

cursor.execute(sqlCreate)
print("Table Wind created successfully........")
#############################################################
sqlCreate = """
           CREATE TABLE Sun (
                SunID SERIAL NOT NULL,
                Sunrise timestamptz NOT NULL,
                Sunset timestamptz NOT NULL,
                CityID int NOT NULL,
                DateTime timestamptz NOT NULL,
                PRIMARY KEY (SunID, DateTime),
				CONSTRAINT fk_city
				  FOREIGN KEY(CityID) 
				  REFERENCES City(CityID)
            )
            """ 

cursor.execute(sqlCreate)
print("Table Sun created successfully........")
#############################################################
sqlCreate = """
           CREATE TABLE Precipitation (
                PrecipitationID SERIAL NOT NULL,
                Description varchar(255),
                vol_1h float,
                vol_3h float,
                CityID int NOT NULL,
                DateTime timestamptz,
                PRIMARY KEY (PrecipitationID, DateTime),
				CONSTRAINT fk_city
				  FOREIGN KEY(CityID) 
				  REFERENCES City(CityID)
            )
            """ 

cursor.execute(sqlCreate)
print("Table Precipitation created successfully........")
#############################################################
sqlCreate = """
           CREATE TABLE MeteorologicalData (
                MeteroID SERIAL NOT NULL,
                Temperature float NOT NULL,
                Temp_min float,
                Temp_max float,
                Presure float NOT NULL,
                Humidity float NOT NULL,
                Description varchar(255),
                visibility float,
                Cloudly int NOT NULL,
                Precipitation boolean NOT NULL,
                CityID int NOT NULL,
                DateTime timestamptz NOT NULL,
                PRIMARY KEY (MeteroID, DateTime),
				CONSTRAINT fk_city
				  FOREIGN KEY(CityID) 
				  REFERENCES City(CityID)
            )
            """ 

cursor.execute(sqlCreate)
print("Table MeteorologicalData created successfully........")
#############################################################
sqlCreate = """
          CREATE TABLE AirQuality (
                AQID SERIAL NOT NULL,
                aqi int NOT NULL,
                o3 float NOT NULL,
                so2 float NOT NULL,
                no2 float NOT NULL,
                co float NOT NULL,
                nh3 float NOT NULL,
                pm25 float NOT NULL,
                pm10 float NOT NULL,
                pollen_tree float,
                pollen_grass float,
                pollen_weed float,
                mold_level float,
                dominant_type varchar(255),
                CityID int NOT NULL,
                DateTime timestamptz NOT NULL,
                PRIMARY KEY (AQID, DateTime),
				        CONSTRAINT fk_city
				        FOREIGN KEY(CityID) 
				        REFERENCES City(CityID)
            )
            """ 

cursor.execute(sqlCreate)
print("Table AirQuality created successfully........")


#Closing the connection
conn.close()