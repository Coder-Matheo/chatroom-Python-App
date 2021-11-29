import requests

#wird die Internet gecheckt, ob internet connection haben
#Lösung die API-Problem für aufrufen


api = "478654d902e9c77a8435368bc6f781bc"
path_weatherIpi = "https://api.openweathermap.org/data/2.5/weather?q="
reg_location = requests.get('https://ipinfo.io/')

def connection_check():
    try:
        requests.get("http://google.com", timeout=3)

        api = "478654d902e9c77a8435368bc6f781bc"
        path_weatherIpi = "https://api.openweathermap.org/data/2.5/weather?q="
        reg_location = requests.get('https://ipinfo.io/')
        return True
    except requests.ConnectionError:
        pass

    return False









