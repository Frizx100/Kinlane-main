import requests

from app.classes.config import API

class Image():
    def __init__(self):
        pass

    def get_icon_by_slug(self, slug: str):
        return requests.get(f'{API}/media/icon/{slug}').content
    
    def get_preview_playlist(self, id: int):
        return requests.get(f'{API}/media/preview/playlist/{id}').content
    
    def get_preview_mediaItem(self, id: int):
        return requests.get(f'{API}/media/preview/mediaItem/{id}').content