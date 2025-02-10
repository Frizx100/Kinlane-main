import requests
from time import localtime, strftime

from app.classes.config import API

class User():
    def __init__(self):
        self.__username: str
        self.__password: str
        self.__authorized: bool = False
        self.__message: str = 'Користувач повинен авторизуватися.'

    def login(self, username, password) -> None:
        if len(username) == 0 or len(password) == 0:
            self.__message = 'Заповніть yci поля!'
        else:
            answer = requests.post(f'{API}/user/login', json={'username': username, 'password': password})
            if answer.ok:
                self.__username = username
                self.__password = password
                self.__authorized = True
                self.__message = 'Успішно авторизовано.'
            else:
                self.logout()
                self.__message = answer.json()['status_message']
    
    def registration(self, username, password_1, password_2) -> None:
        if len(username) == 0 or len(password_1) == 0:
            self.__message = 'Заповніть yci поля!'
        elif password_1 != password_2:
            self.__message = "Паролі повинні збігатися!"
        else:
            answer = requests.post(f'{API}/user/registration', json={'username': username, 'password': password_1})
            if answer.ok:
                self.login(username, password_1)
            else:
                self.logout()
                self.__message = answer.json()['status_message']

    def get_username(self) -> str:
        return self.__username

    def is_authorized(self) -> bool:
        return self.__authorized

    def get_message(self) -> str:
        return self.__message
    
    def logout(self) -> None:
        self.__username = None
        self.__password = None
        self.__authorized = False
        self.__message = 'Користувач повинен авторизуватися.'

    def get_all_playlists_type(self, type: str)->list:
        params = {'type': type, 'user': self.__username}
        answer = requests.get(f'{API}/media/all/playlists/type', params=params)
        if answer.ok:
            return answer.json()['data']
        
    def upload_mediaItem(self, 
                         path_file: str, 
                         playlists_id: list[int], 
                         mediaItem_type: str, 
                         title: str, 
                         description: str)->None:
        file = {'upload_file': open(path_file,'rb'),}
        data = {
            'username': self.__username,
            'playlists_id': '.'.join(playlists_id),
            'mediaItem_type': mediaItem_type,
            'title': title,
            'description': description,
            'time': self.get_local_time()
        }
        answer = requests.post(f'{API}/media/upload/mediaItem', 
                               params=data, 
                               files=file)
        if answer.ok:
            print('save mediaItem')
        else:
            print(answer.json()['status_message'])

    def create_playlist(self, title: str, description: str, format_slug: str, logo_path: str):
        data = {
            'username': self.__username,
            'title': title,
            'description': description,
            'format_slug': format_slug
        }
        if logo_path == '':
            answer = requests.post(f'{API}/media/upload/playlist/without_logo', params=data)
        else:
            file = {'upload_file': open(logo_path,'rb'),}
            answer = requests.post(f'{API}/media/upload/playlist/with_logo', params=data, files=file)
        if answer.ok:
            print('create playlist')
        else:
            print(answer.json()['status_message'])

    def get_local_time(self)->str:
        return strftime('%d.%m.%Y.%H.%M.%S', localtime())
    
    def get_info_playlist_by_id(self, id: int):
        answer = requests.get(f'{API}/media/info/playlist', params={'id': id})
        if answer.ok:
            return answer.json()['data']

    def get_content_playlist_by_id(self, id: int):
        answer = requests.get(f'{API}/media/content/playlist', params={'id': id})
        if answer.ok:
            return answer.json()['data']