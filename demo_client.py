import requests
import json


url = 'http://192.168.1.178:6001/text'


if __name__ == '__main__':
    while True:
        message = input("Enter a test message:")
        response = requests.request(method='POST', url=url, json={'message': message})
        print(response.text)