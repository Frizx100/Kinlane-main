import requests
import os

from app.classes.config import API

class MediaItem():
    def __init__(self):
        pass

    def check_type(self, path: str)->dict:
        status = {
            'status': False,
            'description': 'Упс щось не так з файлом',
            'slug_format': None
        }
        if self.exists_file(path):
            file_extension = None
            supported_formats = self.get_supported_formats()
            file_name = os.path.basename(path).lower()
            for index in range(len(file_name)-1, -1, -1):
                if file_name[index] == '.':
                    file_extension = file_name[index + 1:]
                    break

            for format in supported_formats:
                if file_extension in format[3].split():
                    status['status'] = True
                    status['description'] = 'Ok'
                    status['slug_format'] = format[2]
                    break
            else:
                status['status'] = False
                status['description'] = 'Непідтримуваний формат!'
                status['slug_format'] = None
        else:
            status['status'] = False
            status['description'] = 'Файла не існує!'
            status['slug_format'] = None

        return status
            

    def exists_file(self, path: str)->bool:
        if os.path.isfile(path):
            return True
        else:
            return False
        
    def get_supported_formats(self)->list:
        answer = requests.get(f'{API}/media/supported_formats')
        if answer.ok:
            return answer.json()['data']
        
    def get_info_mediaItem(self, id: int):
        answer = requests.get(f'{API}/media/info/mediaItem', params={'id': id})
        if answer.ok:
            return answer.json()['data']
        
    def get_preview_mediaItem(self, id: int):
        return requests.get(f'{API}/media/preview/mediaItem/{id}').content

    def get_url_video(self):
        return f'{API}/media/video/'
    
    def get_url_music(self):
        return f'{API}/media/music/'