from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from settings import async_session
from services.yandex_oauth_service import Oauth2Service
from services.user_service import UserService
from services.file_service import FileService


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_userservice(session: SessionDep) -> UserService:
    return UserService(session)

user_service = Annotated[UserService, Depends(get_userservice)]


async def get_service(session: SessionDep) -> Oauth2Service:
    return Oauth2Service(session)

oauth2_service = Annotated[Oauth2Service, Depends(get_service)]


async def get_fileservice(session: SessionDep) -> FileService:
    return FileService(session)

file_service = Annotated[FileService, Depends(get_fileservice)]