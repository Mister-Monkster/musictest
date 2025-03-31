from authlib.integrations.starlette_client import OAuth
from sqlalchemy.ext.asyncio import AsyncSession
from auth import create_access_token, create_refresh_token
from settings import client_id, client_secret
from db.queries import add_user_query
from schemas import SRegister


class Oauth2Service:
    def __init__(self,  session: AsyncSession):
        self.session = session
        self.oauth = OAuth()
        self.oauth.register(
            name='yandex',
            client_id=client_id,
            client_secret=client_secret,
            authorize_url='https://oauth.yandex.ru/authorize',
            access_token_url='https://oauth.yandex.ru/token',
            userinfo_endpoint='https://login.yandex.ru/info',
            client_kwargs={
                'scope': 'login:email login:info',
                'response_type': 'code',
            },
        )

    async def register_or_update(self, user):
        user_data = SRegister(
            email=user['default_email'],
            login=user['login'],
            yandex_id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            sex=user['sex'])
        user_model = await add_user_query(user_data, self.session)
        id = user_model
        access_token = create_access_token({'sub': f'{id}'})
        refresh_token = create_refresh_token({'sub': f'{id}'})
        return {"access_token": access_token, "refresh_token": refresh_token}
