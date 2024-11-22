from http.client import HTTPResponse
import json
import os
from fastapi.responses import HTMLResponse, FileResponse
import sys
from a2wsgi import ASGIMiddleware
import uvicorn
from loguru import logger
# from rich import print
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    # get_swagger_ui_oauth2_redirect_html,
)
from apps.api import all_routers
from config import settings


app = FastAPI(
    title="API: Реестр учета ИС/ИР",
	redoc_url=None,
	docs_url=None, 
    debug=settings.DEBUG,
    root_path=settings.ROOT_PATH,
    # root_path="/reestr_is",
    # root_path_in_servers=False,

    # servers=[
    #     {"url": "http://127.0.0.1:8855/reestr_is", "description": "Боевой сервер reestr_is"},
    #     {"url": "http://127.0.0.1:8855/reestr_is/test", "description": "Сервер разработки reestr_is-test"},
    #     {"url": "http://127.0.0.1:5050", "description": "Сервер разработки 1.1"},
    #     {"url": "http://127.0.0.1:5050/reestr_is", "description": "Сервер разработки 1.2"},
        # {"url": "https://tnnc-sppp-app.rosneft.ru:80/reestr_is", "description": "Боевой сервер"}
#     ]
)

"""Обязательно монтируем пути со статическими файлами"""
'''для Свагера'''
# try:
# except:
app.mount("/static", StaticFiles(directory="src/static"), name="static")
# app.mount("/static", StaticFiles(directory="static"), name="static")
    

# app.mount("/src/static", StaticFiles(directory="src/static"), name="static")
'''для фронта'''
# app.mount("/spa", StaticFiles(directory="spa"), name="spa")

'''Для того чтоб файлы стали доступны для скачивания нужно добавить ссылку'''
# app.mount('/download', StaticFiles(directory=settings.ROOT_DIRECTORY_OF_DOCUMENTS), name="download")
# http://127.0.0.1:5050/download/СРК/На отлично.pdf


'''****************************************************************************'''
'''Отправка фронтенда клиенту'''
# @app.get("/", include_in_schema=False)
# async def client():
#     patch = os.path.join('spa/index.html')
#     with open(patch) as file:
#         return HTMLResponse(content=file.read())

@app.get("/", include_in_schema=False)
async def client():
    return HTMLResponse(content="API")
'''****************************************************************************'''
'''Документация приложения'''
@app.get("/docs/", include_in_schema=False)
async def custom_swagger_ui_html():
    logger.success("Подключение")
    logger.success(f"/docs = -------------")
    logger.success(f"app.openapi_url = {app.openapi_url}")
    logger.success(f"app.root_path = {app.root_path}")
    return get_swagger_ui_html(
        openapi_url = app.root_path + app.openapi_url,
        title=app.title + " - Swagger UI",
        # oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"{app.root_path}/static/swagger-ui-bundle.js",
        swagger_css_url=f"{app.root_path}/static/swagger-ui.css",
        swagger_favicon_url=f"{app.root_path}/static/favicon.png",
    )

# @app.get("/redoc", include_in_schema=False)
# async def redoc_html():
#     return get_redoc_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - ReDoc",
#         redoc_js_url="/static/redoc.standalone.js",
#     )

# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()


@app.get("/app")
def read_main(request: Request):
    logger.success('read_main')
    return {
        "message": "Hello World", 
        "root_path": request.scope.get("root_path"),
        "openapi_url": app.openapi_url,
        "base_url": request.base_url,
        }

for router in all_routers:
    app.include_router(router)
'''-----------------------------------------------------------------'''
from fastapi.middleware.cors import CORSMiddleware
origins = [
    # "http://localhost:9000",
    # "http://127.0.0.1:8855",
    # "https://tnnc-sppp-app.rosneft.ru:80/",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin", "Authorization"],
#     allow_methods=["*"],
#     allow_headers=["*"],
)
'''-----------------------------------------------------------------'''
'''Хэширование запросов fastapi'''
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decorator import cache
# from redis import asyncio as aioredis

# @app.on_event("startup")
# async def startup():
    # redis = aioredis.from_url("redis://localhost")
    # redis = aioredis.from_url("redis://localhost:6379")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
'''-----------------------------------------------------------------'''

wsgi_app = ASGIMiddleware(app)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="127.0.0.1", port=5050)


    # sys.exit(wsgi_app)

