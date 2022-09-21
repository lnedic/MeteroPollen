import requests
import config
import pandas as pd
from geopy.geocoders import Nominatim

def CallAirQualityApi(lon, lat, hist, start=0, end=0):
	response_list = []
	#Hist: bool (call history data:true/false)
	if hist:
		url = config.AirQualityApiUrl_HIST
	else:	
		url = config.AirQualityApiUrl

	#lon, lat = FindCityCoord(city)
	querystring = {"lon":lon,"lat":lat}
	headers = {
		"X-RapidAPI-Key": config.X_RapidAPI_Key,
		"X-RapidAPI-Host": config.X_RapidAPI_Host
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response_list.append(response.json())
	df = pd.DataFrame.from_dict(response_list)
	return df

def FindCityCoord(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    # getting Latitude and Longitude
    location = geolocator.geocode(city)
    return (location.longitude, location.latitude)

def Transform_AirQualityData(df):
	air_record = list()
	air_record.append(CalculateAQIindex(df['data'].to_dict()[0][0]['aqi']))
	air_record.append(df['data'].to_dict()[0][0]['o3'])
	air_record.append(df['data'].to_dict()[0][0]['so2'])
	air_record.append(df['data'].to_dict()[0][0]['no2'])
	air_record.append(df['data'].to_dict()[0][0]['co'])
	air_record.append(0.0) #TODO: NH3 dodaj
	air_record.append(df['data'].to_dict()[0][0]['pm25'])
	air_record.append(df['data'].to_dict()[0][0]['pm10'])
	air_record.append(df['data'].to_dict()[0][0]['pollen_level_tree'])
	air_record.append(df['data'].to_dict()[0][0]['pollen_level_grass'])
	air_record.append(df['data'].to_dict()[0][0]['pollen_level_weed'])
	air_record.append(df['data'].to_dict()[0][0]['mold_level'])
	air_record.append(df['data'].to_dict()[0][0]['predominant_pollen_type'])
	air_record = tuple(air_record)
	return air_record


def CalculateAQIindex(aqiValue):
	AQI = 0
	if aqiValue < 51: 
		AQI = 1
	elif aqiValue >50 and aqiValue < 100:
		AQI = 2
	elif aqiValue >100 and aqiValue < 151:
		AQI = 3
	elif aqiValue >150 and aqiValue < 201:
		AQI = 4
	elif aqiValue >200 and aqiValue < 301:
		AQI = 5
	else:
		AQI = 6
	return AQI




# GLAVNI POZIV ZA CURRENT AIRQUALITY -> GOTOVO
#df = CallAirQualityApi(15.966568, 45.815399, False)
#res = Transform_AirQualityData(df)
#print(res)