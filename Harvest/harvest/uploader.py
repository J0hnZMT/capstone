import requests
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
url = 'http://127.0.0.1:5000/harvest/upload'
file_to_open = os.path.join(path, 'browsinghistoryview.zip')
file = {'file': open(file_to_open, 'rb')}

r = requests.post(url, files=file)
print(r.status_code)
print(r.text)


def get_binary(file):
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)



