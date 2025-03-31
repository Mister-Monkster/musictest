from fastapi import APIRouter, UploadFile, HTTPException, Request
from dependencies import file_service
from schemas import SFileGet

files_router = APIRouter(tags=['Файлы', ], prefix='/files')


@files_router.post('/upload', summary='Загурзить файл')
async def upload(request: Request, file: UploadFile, filename: str, service: file_service):
    access_token = request.cookies.get('users_access_token')
    try:
        type = file.headers['content-type']
        extension = file.filename.split('.')[-1]
        if 'audio' in type:
            res = await service.save_file(file, filename, extension, access_token)
            if not res:
                return {'ok': False, 'detail': 'Файл с таким названием уже существует'}
            return {'ok': True, 'detail': 'Файл успешно загружен.'}
        else:
            raise HTTPException(status_code=400, detail='Неверный тип файла')
    except HTTPException:
        raise HTTPException(status_code=401, detail='Not authorize')


@files_router.get('/files', summary='Получить информацию о файлах по ID пользователя')
async def get_files(user_id: int, request: Request, service: file_service) -> list[SFileGet]:
    access_token = request.cookies.get('users_access_token')
    try:
        return await service.get_user_files(user_id, access_token)
    except HTTPException:
        raise (HTTPException(status_code=401, detail='Not authorize'))


@files_router.get('/my-files', summary='Получить информацию о файлах текущего пользователя')
async def get_my_files(request: Request, service: file_service) -> list[SFileGet]:
    access_token = request.cookies.get('users_access_token')
    try:
        if access_token:
            return await service.get_my_files(access_token)
        else:
            raise HTTPException(status_code=401, detail='Not authorize')
    except HTTPException as e:
        raise e
