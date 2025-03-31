import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers.user_router import user_router
from routers.yandex_router import yandex_router
from routers.files_router import files_router


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key='secret')


app.include_router(router=user_router)
app.include_router(router=yandex_router)
app.include_router(router=files_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,

    )
