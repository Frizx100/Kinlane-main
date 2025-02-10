from fastapi import APIRouter, Response, status, Body, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from starlette.responses import StreamingResponse, HTMLResponse
from starlette.requests import Request
from shutil import copyfileobj
from starlette.templating import Jinja2Templates

from db_handler import DataBase
from media.services import get_path_icon_by_slug, open_file

media_router = APIRouter(prefix='/media', tags=["media"])
#templates = Jinja2Templates(directory="static/templates")

# @media_router.post('/all_playlists')
# async def get_all_playlists(request: Request, data=Body()):
#     bd: DataBase = request.app.state.database
#     answer = bd.all_playlist_user(data['user']) 
#     return JSONResponse({'data': answer['data'], 'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.post('/all/history')
async def get_all_history(request: Request, data=Body()):
    bd: DataBase = request.app.state.database
    answer = bd.get_all_history(data['user']) 
    return JSONResponse({'data': answer['data'], 'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.get('/all/playlists/type')
async def get_all_playlists_type(type: str, user: str, request: Request):
    bd: DataBase = request.app.state.database
    answer = bd.get_all_playlists_type(type, user)
    return JSONResponse({'data': answer['data'], 'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.get('/icon/{slug}', response_class=FileResponse)
async def get_icon_by_slug(slug: str):
    return get_path_icon_by_slug(slug)
    
@media_router.get('/preview/playlist/{id}', response_class=FileResponse)
async def get_preview_playlist(id: int, request: Request):
    bd: DataBase = request.app.state.database
    path = bd.get_preview_playlist(id)
    return path

@media_router.get('/preview/mediaItem/{id}', response_class=FileResponse)
async def get_preview_mediaItem(id: int, request: Request):
    bd: DataBase = request.app.state.database
    path = bd.get_preview_mediaItem(id)
    return path

@media_router.get('/supported_formats')
async def get_supported_formats(request: Request):
    bd: DataBase = request.app.state.database
    answer = bd.get_supported_formats()
    return JSONResponse({'data': answer['data'], 'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.post('/upload/mediaItem', tags=["Upload"])
async def upload_mediaItem(request: Request, 
                            time: str,
                            username: str,
                            playlists_id: str,
                            mediaItem_type: str,
                            title: str,
                            description: str,
                            upload_file: UploadFile=File(...)):
    bd: DataBase = request.app.state.database
    upload_file.filename = upload_file.filename.lower()
    path = bd.get_path_to_save_files(username, mediaItem_type, upload_file.filename)
    with open(path, 'wb+') as buffer:
        copyfileobj(upload_file.file, buffer)

    if playlists_id == '':
        playlists_id: list[int] = []
    else:
        buf_playlists = playlists_id.split('.')
        playlists_id: list[int] = []
        for playlist in buf_playlists:
            playlists_id.append(int(playlist))

    answer = bd.save_mediaItem(username, playlists_id, mediaItem_type, title, description, time, path)
    return JSONResponse({'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.post('/upload/playlist/with_logo', tags=["Upload"])
async def upload_playlist_with_logo(request: Request,
                                    username: str,
                                    title: str,
                                    description: str,
                                    format_slug: str,
                                    upload_file: UploadFile=File(...)):
    bd: DataBase = request.app.state.database
    upload_file.filename = upload_file.filename.lower()
    path = bd.get_path_to_save_files(username, format_slug, upload_file.filename)
    with open(path, 'wb+') as buffer:
        copyfileobj(upload_file.file, buffer)
    
    answer = bd.create_playlist(username, title, description, format_slug, path)
    return JSONResponse({'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.post('/upload/playlist/without_logo')
async def upload_playlist_without_logo(request: Request,
                                    username: str,
                                    title: str,
                                    description: str,
                                    format_slug: str):
    bd: DataBase = request.app.state.database
    path_logo = get_path_icon_by_slug(format_slug)
    answer = bd.create_playlist(username, title, description, format_slug, path_logo)
    return JSONResponse({'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.get('/info/playlist')
async def get_info_playlist(id: int, request: Request):
    bd: DataBase = request.app.state.database
    answer = bd.get_info_playlist(id)
    return JSONResponse({'data': answer['data'], 'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.get('/content/playlist')
async def get_content_playlist(id: int, request: Request):
    bd: DataBase = request.app.state.database
    answer = bd.get_content_playlist(id)
    return JSONResponse({'data': answer['data'], 'status_message': answer['status_message']}, status_code=answer['status'])



#@media_router.get("/index/{video_pk}", response_class=HTMLResponse)
#async def get_test_video(request: Request, video_pk: int):
 #   return templates.TemplateResponse("index.html", {"request": request, "path": video_pk})

@media_router.get('/info/mediaItem')
async def get_info_mediaItem(id: int, request: Request):
    bd: DataBase = request.app.state.database
    answer = bd.get_info_mediaItem(id)
    return JSONResponse({'data': answer['data'], 'status_message': answer['status_message']}, status_code=answer['status'])

@media_router.get("/video/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    bd: DataBase = request.app.state.database
    path = bd.get_path_mediaItem(video_pk)
    file, status_code, content_length, headers = await open_file(request, path)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response

@media_router.get("/music/{music_id}")
async def get_streaming_music(request: Request, music_id: int) -> StreamingResponse:
    bd: DataBase = request.app.state.database
    path = bd.get_path_mediaItem(music_id)
    file, status_code, content_length, headers = await open_file(request, path)
    response = StreamingResponse(
        file,
        media_type='audio/mpeg',
        status_code=status_code
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response