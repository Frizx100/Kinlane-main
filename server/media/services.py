import os
from pathlib import Path
from typing import IO, Generator
from starlette.requests import Request

def file_valid(path: str)->str:
    if os.path.exists(path):
        return path
    else:
        return 'static/icons/not_found.png'
    
def get_path_icon_by_slug(slug: str)->str:
    icons = {
        'add': 'static/icons/add.png',
        'photo': 'static/icons/camera.png',
        'history': 'static/icons/history.png',
        'music': 'static/icons/music.png',
        'profile': 'static/icons/profile.png',
        'setting': 'static/icons/setting.png',
        'video': 'static/icons/video.png',
        'full_screen': 'static/icons/full_screen.png',
        'previous': 'static/icons/previous.png',
        'minimize': 'static/icons/minimize.png',
        'next': 'static/icons/next.png',
        'pause': 'static/icons/pause.png',
        'play': 'static/icons/play.png',
        'volume': 'static/icons/volume.png'
    }
    if slug in icons:
        path = icons[slug]
    else:
        print(slug)
        path = 'static/icons/not_found.png'
    return path

def ranged(file: IO[bytes], start: int = 0, end: int = None, block_size: int = 8192) -> Generator[bytes, None, None]:
    consumed = 0
    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data
    if hasattr(file, 'close'):
        file.close()


async def open_file(request: Request, path_mediaItem: str) -> tuple:
    #path = Path('static/media/161a68601ec1d8ca45250557cff3ffb98eca53fbcf86bbdb8e8bb6e7/video/f5e859b8-8e5c-41a4-9382-d33f2cfe9caf.mp4') #Factorio
    #path = Path('static/media/161a68601ec1d8ca45250557cff3ffb98eca53fbcf86bbdb8e8bb6e7/video/2f49bd9c-b8bf-418e-9b5f-2cdc0b7a6040.mp4') #Mikury
    #path = Path('static/media/161a68601ec1d8ca45250557cff3ffb98eca53fbcf86bbdb8e8bb6e7/music/7dd3cc00-a34e-4978-bdd7-6aa4322cbb10.mp3')
    path = Path(path_mediaItem)
    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    headers = {}
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers