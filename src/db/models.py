import enum
from typing import Optional, Annotated

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Genders(enum.Enum):
    male = 'male'
    female = 'female'


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[pk]
    yandex_id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    login: Mapped[str] = mapped_column(String(96), index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    sex: Mapped[Optional[Genders]]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    files_rel: Mapped[list['FileModel']] = relationship(back_populates="user_rel")


class FileModel(Base):
    __tablename__ = 'files'

    id: Mapped[pk]
    filename: Mapped[str] = mapped_column(String(128), index=True)
    dir: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    user_rel: Mapped['UserModel'] = relationship(back_populates='files_rel')
