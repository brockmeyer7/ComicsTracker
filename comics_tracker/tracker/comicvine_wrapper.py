import dotenv, os
import requests
import urllib.parse
import json

class ComicVine():

    def __init__(self):
        dotenv.load_dotenv(os.path.expanduser('~/Documents/Personal_Projects/.env'))
        cv_api_key = os.getenv('COMICVINE_API_KEY')
        self.api_key = f'?api_key={cv_api_key}'
        self.api_url = 'https://comicvine.gamespot.com/api'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    def search(self, **kwargs):
        url = f'{self.api_url}/search/{self.api_key}'
        for k, v in kwargs.items():
            url += f'&{urllib.parse.quote(k)}={urllib.parse.quote(v)}'
        url += '&format=json&limit=20'
        response = requests.get(url, headers=self.headers).json()
        if response['status_code'] == 1:
            return json.dumps(response)
        else:
            return json.dumps(response['status_code'])
    
    def get_issues(self, **kwargs):
        url = f'{self.api_url}/issues/{self.api_key}&filter='
        for k, v in kwargs.items():
            url += f'{k}:{urllib.parse.quote(v)}'
        url += '&format=json&limit=20'
        print(url)
        response = requests.get(url, headers=self.headers).json()
        if response['status_code'] == 1:
            return json.dumps(response)
        else:
            return response['status_code']


    def get_series(self, name: str, offset: int = 0, limit: int = 20, params: list=[]):
        url = f'{self.api_url}/volumes/{self.api_key}&format=json&limit={str(limit)}&offset={offset}&filter=name:{urllib.parse.quote(name)}&field_list='
        print(url)
        for i in range(len(params)):
            if i == 0:
                url += params[i]
            else:
                url += ',' + params[i]
        try:
            response = requests.get(url, headers=self.headers).json()
        except:
            return -1
        
        if response['status_code'] == 1:
            return json.dumps(response)
        else:
            return response['status_code']
        
    def filter_start_year(self, start_year: int, unfilt_list: list):
        results = []
        for item in unfilt_list:
            if item['start_year'] == str(start_year):
                results.append(item)
        return results

    def filter_publisher(self, publisher: str, unfilt_list: list):
        results = []
        for item in unfilt_list:
            if item['publisher']['name'] == publisher:
                results.append(item)
        return results

if __name__ == '__main__':
    cv = ComicVine()
    response = json.loads(cv.get_series(name='Black Widow', offset=0, params=['id', 'name', 'description', 'image']))
    for item in response['results']:
        print(item['id'])
