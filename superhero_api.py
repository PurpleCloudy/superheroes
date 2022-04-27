import os
import json
from xml.dom import NotFoundErr
import requests
import pprint
from get_all_heroes import get_data

directory_list = os.listdir()

if not 'heroes_data.json' in directory_list:
    get_data()

with open('heroes_data.json', 'r+') as f:
    heroes_data = json.loads(f.read())

pp = pprint.PrettyPrinter(indent=4)

API_KEY = '10218686935504422'

with open ('heroes_data.json', 'r+') as f:
    heroes_data = json.loads(f.read())

class SuperHeroAPI:
    def __init__(self, API = API_KEY, data = heroes_data):
        self._token = API
        self._data = data
        self._url = f'https://superheroapi.com/api/{self._token}'
        self.image = f'https://superheroapi.com/api/image/{self._token}'

    def get_hero(self, name):
        name = self._parse_name(name)
        hero_id = self._get_id(name)
        return self._parse_api(self._url + f'/{hero_id}')
    
    def get_hero_stats(self, name):
        name = self._parse_name(name)
        hero_id = self._get_id(name)
        return self._parse_api(self._url + f'/{hero_id}/powerstats')

    def _parse_name(self, name):
        return name.lower().title() 

    def _get_id(self, name):
        data = self._data.get(name, False)
        if data:
            return data
        else:
            raise NotFoundError('Name not found')

    def _parse_api(self, url):
        response = requests.get(url, timeout = 5)
        response.close()
        return response.json()

    def download_image(self, name):
        image_url = self.get_hero_image_url(name)
    
    def get_hero_image_url(self, name):
        name = self._parse_name(name)
        hero_id = self._get_id(name)
        return self._parse_api(self._url + f'/{hero_id}/image')['url']

    def download_image(self, name):
        image_url = self.get_hero_image_url(name)
        with open(f'{name}.jpg','wb') as f:
            response = requests.get(image_url).content
            f.write(response)

class NotFoundError(Exception):
    pass

s = SuperHeroAPI()
result = s.get_hero_image_url('superman')
pp.pprint(result)
s.download_image('superman')