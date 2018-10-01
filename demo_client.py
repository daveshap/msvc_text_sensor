import requests
import json


if __name__ == '__main__':
    while True:
        messag3 = input("Enter a test message:")
        response = requests.request(method='POST', url='127.0.0.1:6001/text', json={'message': "hey how's it going?"})
        print(response.text)