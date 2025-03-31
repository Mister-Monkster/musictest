from fastapi import APIRouter, HTTPException, Response, Request
from dependencies import user_service

from schemas import SChange, SRegister, SUser


user_router = APIRouter(tags=['Пользователи',], prefix='/user')


@user_router.post('/refresh', summary="Обновление токена доступа ♻️")
async def refresh_access_token(request: Request, response: Response, service: user_service) -> SUser:
    refresh_token = request.cookies.get('users_refresh_token')
    try:
        user_data = await service.refresh(refresh_token)
        access_token = user_data['access_token']
        response.set_cookie(key='users_access_token',
                            value=access_token,
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=900)
        return user_data['user']
    except:
        raise HTTPException(status_code=401, detail="Not authorize")


@user_router.post('/logout', summary='Выход❌')
async def logout(response: Response) -> dict:
    response.delete_cookie(key='users_access_token', httponly=True, samesite='lax', secure=False)
    response.delete_cookie(key='users_refresh_token', httponly=True, samesite='lax', secure=False)

    return {"ok": True}


@user_router.get("/profile", summary='Получить данные')
async def get_user(request: Request, service: user_service) -> SRegister:
    access_token = request.cookies.get('users_access_token')
    try:
        return await service.get_user_profile(access_token)
    except:
        raise HTTPException(status_code=401, detail="Not authorize")


@user_router.put('/update', summary='Изменение данных✏️')
async def update_user(requset: Request, response: Response, user_data: SChange, service: user_service):
    access_token = requset.cookies.get('users_access_token')
    try:
        res = await service.update_user_data(access_token, user_data)
        if res:
            return {'ok': True, 'detail': "Данные успешно изменены"}
        else:
            return HTTPException(status_code=response.status_code, detail='Ошибка изменения данных')
    except:
        raise HTTPException(status_code=401, detail="Not authorize")


@user_router.delete('/{id}/delete', summary='Удаление данных❌')
async def delete_user(request: Request, id: int, service: user_service):
    access_token = request.cookies.get('users_access_token')
    try:
        res = await service.delete_user_data(access_token, id)
        if not res:
            raise HTTPException(status_code=403, detail='No access')
        else:
            return {'ok': True, 'detail': 'Пользователь успешно удален'}
    except:
        raise HTTPException(status_code=401, detail='Not authorize')


@user_router.post('user/{id}/create-superuser', summary='Выдать права суперюзера')
async def create_superuser(request: Request, id: int, service: user_service):
    access_token = request.cookies.get('users_access_token')
    try:
        res = await service.create_admin(access_token, id)
        if not res:
            raise HTTPException(status_code=403, detail='No access')
        else:
            return {'ok': True, 'detail': f'Вы выдали права администратора пользователю с id {id}'}
    except:
        raise HTTPException(status_code=401, detail='Not authorize')

