import secrets

from authlib.integrations.base_client import OAuthError
from fastapi import HTTPException

from fastapi import APIRouter, Response
from starlette.requests import Request
from starlette.responses import RedirectResponse
from dependencies import oauth2_service

from schemas import SRegister

yandex_router = APIRouter(tags=['Yandex Oauth2'])


@yandex_router.get('/yandex', summary='Аутентификация через Яндекс')
async def yandex_auth(request: Request, service: oauth2_service):
    redirect_uri = "http://127.0.0.1:8000/auth"
    return await service.oauth.yandex.authorize_redirect(request, redirect_uri)


@yandex_router.get('/auth', summary='Аутентификация через Яндекс')
async def yandex_auth_callback(request: Request, service: oauth2_service):
    try:
        token = await service.oauth.yandex.authorize_access_token(request)
        user = await service.oauth.yandex.get('https://login.yandex.ru/info?format=json', token=token)
        user_json = user.json()
        tokens = await service.register_or_update(user_json)
        if not user:
            raise HTTPException(status_code=400, detail="Не удалось получить данные пользователя")

        response = RedirectResponse(url='/docs', status_code=303)
        response.set_cookie(key='users_refresh_token',
                            value=tokens['refresh_token'],
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=604800)
        response.set_cookie(key='users_access_token',
                            value=tokens['access_token'],
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=900)
        return response

    except OAuthError as e:
        raise HTTPException(status_code=400, detail=str(e))

