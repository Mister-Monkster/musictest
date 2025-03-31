from sqlalchemy.ext.asyncio import AsyncSession
from auth import create_access_token, decode_token
from db.queries import get_user_by_id, update_user_data_query, delete_user_query, create_superuser_query
from schemas import SChange, SRegister, SUser


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def refresh(self, refresh_token: str):
        payload = decode_token(refresh_token)
        user_id = int(payload['sub'])
        user_data = await get_user_by_id(user_id, self.session)
        if payload is None:
            return {"status_code": 401, "detail": 'Невалидный токен'}
        access_token = create_access_token({"sub": f'{user_data.id}'})
        user_dict = SRegister.model_validate(user_data).model_dump(exclude_unset=True)
        return {"user": user_data, "access_token": access_token}

    async def get_user_profile(self, access_token: str):
        payload = decode_token(access_token)
        user_id = int(payload['sub'])
        user_data = await get_user_by_id(user_id, self.session)
        return user_data

    async def update_user_data(self, access_token: str, new_data: SChange):
        try:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            await update_user_data_query(user_id, new_data, self.session)
            return True
        except Exception:
            raise Exception

    async def delete_user_data(self, access_token: str, id: int):
        payload = decode_token(access_token)
        user_id = int(payload['sub'])
        user = await get_user_by_id(user_id, self.session)
        if not user.is_superuser:
            return None
        else:
            await delete_user_query(id, self.session)
            return True

    async def create_admin(self, access_token: str, id: int):
        payload = decode_token(access_token)
        user_id = int(payload['sub'])
        user = await get_user_by_id(user_id, self.session)
        if not user.is_superuser:
            return None
        else:
            await create_superuser_query(id, self.session)
            return True

