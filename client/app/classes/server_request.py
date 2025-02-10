import requests
#from requests.api import request

API = 'http://127.0.0.1:3222'

def login(username: str, password: str)->requests:
    return requests.post(f'{API}/user/login', json={'username': username, 'password': password})

def registration(username: str, password: str)->requests:
    return requests.post(f'{API}/user/registration', json={'username': username, 'password': password})

def get_all_playlists(user):
    return requests.post(f'{API}/media/home_page', json={'user': user})
