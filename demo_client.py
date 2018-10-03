import requests


if __name__ == '__main__':
    url = 'http://192.168.1.178:6001/text'
    while True:
        message = input("Enter a test message:")
        response = requests.request(method='POST', url=url, json={'data': message})
        print(response.text)