from pydantic import BaseModel


class SChange(BaseModel):
    first_name: str
    last_name: str
    sex: str | None = None


class SRegister(SChange):
    login: str
    email: str
    yandex_id: int

    class Config:
        extra = "ignore"
        from_attributes = True


class SUser(SRegister):
    is_superuser: bool


class SFileGet(BaseModel):
    filename: str
    dir: str

    class Config:
        extra = "ignore"
        from_attributes = True


class SFile(SFileGet):
    user_id: int




