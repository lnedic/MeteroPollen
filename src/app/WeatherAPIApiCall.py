import requests

url = "https://weatherapi-com.p.rapidapi.com/current.json"

querystring = {"q":"Novi Sad"}

headers = {
	"X-RapidAPI-Key": "45890264e1msh908d45da5462129p195224jsne758b9056578",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


# DOBAR TRASFORMIRAJ I PROVJERI HISTORY