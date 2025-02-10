import os
from datetime import datetime

import hashlib
import psycopg
from fastapi import status
from uuid import uuid4

from db_config import HOST, USER, PASSWORD, DB, PORT, MASTER_PATH
from media.services import file_valid

class DataBase():
    def __init__(self):
        self.connection = psycopg.connect(
            f'dbname={DB} user={USER} host={HOST} port={PORT} password={PASSWORD}'
        )
        self.connection.autocommit = False

    def convert_to_hash(self, data: str) -> str:
        hash_data = hashlib.sha224(data.encode())
        return hash_data.hexdigest()

    def login(self, user: str, password: str) -> dict:
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select*
                From "User"
                Where username='{user}';
                '''
            )
            value = cur.fetchall()
            if value and value[0][2] == self.convert_to_hash(password):
                return {'status': 200, 'status_message': "Користувач автентифікований"}
            else:
                return {'status': 403, 'status_message': "Будь ласка, перевірте свій пароль та ім'я облікового запису i спробуйте знову."}
    
    def registration(self, username: str, password: str) -> dict:
        with self.connection.cursor() as cur:
            try:
                cur.execute(
                    f'''
                    Select "username"
                    From "User";
                    '''
                )
                value = cur.fetchall()
                taken_usernames = [item[0] for item in value]
                if username in taken_usernames:
                    return{'status': 400, 'status_message': "Такий користувач вже існує."}

                cur.execute(
                    f'''
                    Insert Into "User" ("username", "password")
                    Values ('{username}', '{self.convert_to_hash(password)}');
                    '''
                )
                self.connection.commit()

                cur.execute(
                    f'''
                    Select*
                    From "User"
                    Where username='{username}';
                    '''
                )
                value = cur.fetchall()
                user_id: str = value[0][0]

                cur.execute(
                    f'''
                    Select *
                    From "Format"
                    '''
                )
                all_formats = cur.fetchall()
                full_path = os.path.join(MASTER_PATH, self.convert_to_hash(str(user_id)))
                os.mkdir(full_path)
                for format in all_formats:
                    id_format = format[0]
                    logo = format[3]
                    title_format = format[1]
                    folder_for_specific_file = format[4]
                    folder = os.path.join(full_path, folder_for_specific_file)
                    os.mkdir(folder)
                    cur.execute(
                        f'''
                        Insert Into "Playlists" ("title", "id_user", "id_format", "logo")
                        Values ('{title_format}', {user_id}, {id_format}, {logo});
                        '''
                    )
                    self.connection.commit()
                return{'status': 201, 'status_message': "Користувач створено."}
            except psycopg.errors.UniqueViolation:
                self.connection.rollback()
                return{'status': 400, 'status_message': "Такий користувач вже існує."}
            except Exception as _ex:
                print(f'ex: {_ex}')
                self.connection.rollback()
                return{'status': 500, 'status_message': "Виникла помилка на сервері, спробуйте повторити спробу пізніше."}
    
    def get_user_id(self, username: str)->int:
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select "id"
                From "User"
                Where "username" = '{username}'
                '''
            )
            user_id = cur.fetchone()[0]
            return int(user_id)
        
    def get_format_id_by_slug(self, slug: str) -> int:
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select "id"
                From "Format"
                Where "slug" = '{slug}'
                '''
            )
            format_id = cur.fetchone()[0]
            return int(format_id)

    def get_all_history(self, user):
        with self.connection.cursor() as cur:
            user_id = self.get_user_id(user)
            cur.execute(
                f'''
                Select mi.id, mi.title, mi.description, mi.logo, mi.path
                From "RecentlyViewed" rv
                Inner Join "MediaItem" mi ON rv.id_Item = mi.id
                Where rv.id_user = {user_id}
                '''
            )
            value = cur.fetchall()
            return {'data': value, 'status': status.HTTP_200_OK, 'status_message': "Ok."}
        
    def get_all_playlists_type(self, type: str, user: str):
        with self.connection.cursor() as cur:
            user_id = self.get_user_id(user)
            cur.execute(
                f'''
                Select pl.id, pl.title, pl.description, (Select count(plr.id) From "PlaylistsRelation" plr Where plr.id_playlists = pl.id)
                From "Playlists" pl
                Inner Join "Format" f on pl.id_format = f.id
                Where (pl.id_user = {user_id}) and (f.slug = '{type}');
                '''
            )
            value = cur.fetchall()
            return {'data': value, 'status': status.HTTP_200_OK, 'status_message': "Ok."}
    
    def get_preview_playlist(self, id: int) -> str:
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select pl.logo
                From "Playlists" pl
                Where pl.id = {id};
                '''
            )
            value = cur.fetchone()[0]
            return file_valid(value)
            
    def get_preview_mediaItem(self, id: int) -> str:
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select mi.logo
                From "MediaItem" mi
                Where mi.id = {id};
                '''
            )
            value = cur.fetchone()[0]
            return file_valid(value)

    def get_supported_formats(self)->list:
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select f.id, f.title, f.slug, f.supported_formats
                From "Format" f
                '''
            )
            value = cur.fetchall()
            return {'data': value, 'status': status.HTTP_200_OK, 'status_message': "Ok."}
    
    def get_path_to_save_files(self, username: str, format_slug: str, file_name: str)->str:
        user_id = self.get_user_id(username)

        for index in range(len(file_name)-1, -1, -1):
            if file_name[index] == '.':
                name = str(uuid4()) + file_name[index:]
                break
        
        path = os.path.join(MASTER_PATH, self.convert_to_hash(str(user_id)), format_slug, name)
        return path
    
    def save_mediaItem(self, username: str, playlists_id: list[int], slug_type: str, title: str, description: str, time: str, path_file: str):
        user_id = self.get_user_id(username)
        with self.connection.cursor() as cur:
            try:
                if len(playlists_id) == 0:
                    cur.execute(
                        f'''
                        Select pl.id
                        From "Playlists" pl
                        Inner Join "Format" f on pl.id_format = f.id
                        Where f.slug = '{slug_type}' and pl.id_user = {user_id}
                        '''
                    )
                    playlists_id.append(int(cur.fetchone()[0]))
                if slug_type == 'photo':
                    logo_path = path_file
                else:
                    icons = {
                        'music': 'static/icons/music.png',
                        'video': 'static/icons/video.png',
                    }
                    if slug_type in icons:
                        logo_path = icons[slug_type]
                    else:
                        logo_path = 'static/icons/not_found.png'
                time = time[:10] + " " + time[11:13] + ":" + time[14:16] + ":" + time[17:]

                cur.execute(
                    f'''
                    Select f.id 
                    From "Format" f 
                    Where f.slug = 'video'
                    '''
                )
                id_format = int(cur.fetchone()[0])
                cur.execute(
                    f'''
                    Insert Into "MediaItem" ("title", "description", "path", "logo", "added_at", "id_user", "id_format")
                    Values ('{title}', '{description}', '{path_file}', '{logo_path}', '{time}', '{user_id}', '{id_format}');
                    '''
                )
                self.connection.commit()
                cur.execute(
                    f'''
                    Select mi.id
                    From "MediaItem" mi
                    Where mi.title = '{title}' and mi.path = '{path_file}' and mi.added_at = '{time}' and mi.id_user = '{user_id}'
                    '''
                )
                mediaItem_id = int(cur.fetchone()[0])
                for id_playlist in playlists_id:
                    cur.execute(
                    f'''
                    Insert Into "PlaylistsRelation" ("id_playlists", "id_item")
                    Values ('{id_playlist}', '{mediaItem_id}')
                    '''
                    )
                    self.connection.commit()
                return{'status': status.HTTP_201_CREATED, 'status_message': "mediaItem добавлено."}
            except Exception as _ex:
                print(f'ex: {_ex}')
                self.connection.rollback()
                return{'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status_message': "Виникла помилка на сервері, спробуйте повторити спробу пізніше."} 
            
    def create_playlist(self, username: str, title: str, description: str, format_slug: str, path_logo: str):
        user_id = self.get_user_id(username)
        format_id = self.get_format_id_by_slug(format_slug)
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Insert Into "Playlists" ("title", "logo", "id_user", "id_format", "description")
                Values ('{title}', '{path_logo}', '{user_id}', '{format_id}', '{description}')
                '''
            )
            self.connection.commit()
            return{'status': status.HTTP_201_CREATED, 'status_message': "playlist створено."}
        
    def get_info_playlist(self, id: int):
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select pl.title, pl.description, f.slug as slug_format
                From "Playlists" pl
                Inner Join "Format" f on pl.id_format = f.id
                Where pl.id = {id}
                '''
            )
            data = cur.fetchone()
            value = {
                'title': data[0],
                'description': data[1],
                'slug_format': data[2]
            }
            return{'data': value, 'status': status.HTTP_200_OK, 'status_message': "ok"}

    def get_content_playlist(self, id: int): #id title description slug_format
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select mi.id, mi.title, mi.description, f.slug as slug_format
                From "PlaylistsRelation" plr
                Inner Join "MediaItem" mi on plr.id_item = mi.id
                Inner Join "Format" f on mi.id_format = f.id
                Where plr.id_playlists = {id}
                '''
            )
            data = cur.fetchall()
            return{'data': data, 'status': status.HTTP_200_OK, 'status_message': "playlist створено."}
        
    def get_info_mediaItem(self, id: int):
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select mi.title, mi.description, mi.added_at
                From "MediaItem" mi
                Where mi.id = {id}
                '''
            )
            value: tuple = cur.fetchone()
            t: datetime = value[2]
            data = {
                'title': value[0],
                'description': value[1],
                'date': t.strftime('%d.%m.%Y.%H.%M.%S')
            }
            return{'data': data, 'status': status.HTTP_200_OK, 'status_message': "mediaItem info."}
        
    def get_path_mediaItem(self, id: int) -> str:
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                Select mi.path
                From "MediaItem" mi
                Where mi.id = {id}
                '''
            )
            path = cur.fetchone()[0]
            return path

    def close(self)->None:
        if self.connection:
            self.connection.close()
