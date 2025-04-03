import os

from sqlalchemy.ext.asyncio import AsyncSession
from schemas import SFile, SFileGet
from auth import decode_token
from db.queries import create_file_query, get_files_query


class FileService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_file(self, file, filename: str, access_token: str):
        type = file.headers['content-type']
        extension = file.filename.split('.')[-1]
        if 'audio' in type:
            payload = decode_token(access_token)
            user_id = int(payload['sub'])
            dir = f'./files/{user_id}/{filename}.{extension}'
            dir_name = os.path.dirname(dir)
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            elif os.path.exists(dir):
                return False
            async with open(dir, "wb") as f:
                await f.write(await file.read())
            file_schema = SFile.model_validate({'filename': f'{filename}.{extension}', 'dir': dir, 'user_id': user_id})
            await create_file_query(file_schema, self.session)
        else:
            return False

    async def get_user_files(self, user_id: int) -> list[SFileGet]:
        res = await get_files_query(user_id, self.session)
        result = [SFileGet.model_validate(item, from_attributes=True) for item in res]
        return result

    async def get_my_files(self, access_token: str) -> list[SFileGet]:
        payload = decode_token(access_token)
        user_id = int(payload['sub'])
        res = await get_files_query(user_id, self.session)
        result = [SFileGet.model_validate(item, from_attributes=True) for item in res]
        return result
