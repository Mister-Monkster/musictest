from sqlalchemy import update, select, func, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserModel, FileModel
from schemas import SChange, SRegister, SFile


async def get_user_by_id(user_id: int, session: AsyncSession):
    query = select(UserModel).where(UserModel.id == user_id)
    res = await session.execute(query)
    user_data = res.scalars().one_or_none()
    return user_data


async def update_user_data_query(user_id: int, new_data: SChange, session: AsyncSession):
    values = new_data.model_dump()
    query = update(UserModel).where(UserModel.id == user_id).values(values)
    await session.execute(query)
    await session.commit()


async def add_user_query(user: SRegister, session: AsyncSession):
    data = user.model_dump()
    query = (
        insert(UserModel)
        .values(**data)
        .on_conflict_do_update(
            index_elements=["yandex_id"],
            set_=user.model_dump()
        )
        .returning(UserModel.id)
    )

    result = await session.execute(query)
    await session.commit()
    return result.scalars().one()


async def delete_user_query(id: int, session: AsyncSession):
    query = delete(UserModel).where(UserModel.id == id, UserModel.is_superuser == False)
    await session.execute(query)
    await session.commit()


async def create_superuser_query(id:int, session: AsyncSession):
    query = update(UserModel).values(is_superuser=True).where(UserModel.id == id)
    await session.execute(query)
    await session.commit()


async def create_file_query(file: SFile, session: AsyncSession):
    file_dict = file.model_dump()
    new_file = FileModel(**file_dict)
    session.add(new_file)
    await session.commit()


async def get_files_query(user_id: int, session: AsyncSession):
    query = select(FileModel.filename, FileModel.dir).where(FileModel.user_id==user_id)
    res = await session.execute(query)
    return res.all()
