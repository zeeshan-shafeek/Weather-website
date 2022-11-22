import requests
from pprint import pprint


class WeatherApp:
    def __init__(self, city, units):
        key = open("key.txt", "r")
        self.api_key = key.read()
        key.close()
        self.status = ''
        self.url = 'https://api.openweathermap.org/data/2.5/weather?q='
        self.reply = {}
        self.city = city
        self.units = units
        self.reply = requests.get(f"{self.url}{self.city}&appid={self.api_key}&units={self.units}")
        try:
            self.city = self.reply.json()['name']
        except KeyError:
            pass
        if self.reply.status_code != 200:
            self.status = 'City not found!'

    def request_data(self):
        self.reply = requests.get(f"{self.url}{self.city}&appid={self.api_key}&units={self.units}")

    def check_temp(self):
        self.request_data()
        return self.reply.json()['main']['temp']
