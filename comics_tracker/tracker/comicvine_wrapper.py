import dotenv, os
import requests
import urllib.parse
import json

class ComicVine():

    def __init__(self):
        dotenv.load_dotenv(os.path.expanduser('~/Documents/Personal_Projects/.env'))
        cv_api_key = os.getenv('COMICVINE_API_KEY')
        self.api_key = f'{cv_api_key}'
        self.api_url = 'https://comicvine.gamespot.com/api/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    def search(self, params={}):
        url = self.api_url + 'search/?api_key=' + self.api_key
        for k, v in params.items():
            filter_string = k + '=' + v
            url += '&' + urllib.parse.quote(filter_string, safe='=')
        url += '&format=json'
        response = requests.get(url, headers=self.headers)
        print(response.json())

if __name__ == '__main__':
    cv = ComicVine()
    cv.search(params={'query': 'Black Widow', 'resources': 'volume'})