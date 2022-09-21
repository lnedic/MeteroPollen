from SyncData import SyncData
import config
# 1. option
#import sys
#city = str(sys.argv[1])

# 2. option
#city = input("Unesite grad za koji želite učitavati podatke u bazu: ")

# 3. option

for city in config.city_for_sync:
    print(city, end =" ")
    SyncData(city)

