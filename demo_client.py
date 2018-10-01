import requests
import json


if __name__ == '__main__':
    while True:
        message = input("Enter a test message:")
        response = requests.request(method='POST', url='http://127.0.0.1:6001/text', json={'message': message})
        print(response.text)