import dotenv, os
import requests
import urllib.parse
import json

class ComicVine():

    def __init__(self):
        dotenv.load_dotenv(os.path.expanduser('~/Documents/Personal_Projects/.env'))
        cv_api_key = os.getenv('COMICVINE_API_KEY')
        self.api_key = f'?api_key={cv_api_key}'
        self.api_url = 'https://comicvine.gamespot.com/api/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    def search(self, **kwargs):
        url = f'{self.api_url}search/{self.api_key}'
        for k, v in kwargs.items():
            url += f'&{urllib.parse.quote(k)}={urllib.parse.quote(v)}'
        url += '&format=json&limit=20'
        response = requests.get(url, headers=self.headers).json()
        if response['status_code'] == 1:
            return json.dumps(response)
        else:
            return json.dumps(response['status_code'])
    
    def get_issues(self, **kwargs):
        url = f'{self.api_url}issues/{self.api_key}&filter='
        for k, v in kwargs.items():
            url += f'&{k}={urllib.parse.quote(v)}'
        url += '&format=json&limit=20'
        response = requests.get(url, headers=self.headers).json()
        if response['status_code'] == 1:
            return json.dumps(response)
        else:
            return response['status_code']


    def get_volume(self, name: str, start_year: str, *args):
        url = f'{self.api_url}volumes/{self.api_key}&format=json&filter=name:{urllib.parse.quote(name)}&field_list='
        for i in range(len(args)):
            if i == 0:
                url += args[i]
            else:
                url += ',' + args[i]
        response = requests.get(url, headers=self.headers).json()
        if response['status_code'] == 1:
            result = []
            for item in response['results']:
                if item['start_year'] == start_year and item['name'] == name:
                    result.append(item)
            return json.dumps(item)
        else:
            return response['status_code']
        

if __name__ == '__main__':
    cv = ComicVine()
    response = json.loads(cv.get_volume(name='Black Widow'))
    print(response)
