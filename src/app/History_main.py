from InsertHistoryData import LoadHistoryInDatabase
import sys
city = str(sys.argv[1])

if city == '':
    city = 'Novi Sad'


LoadHistoryInDatabase(city)