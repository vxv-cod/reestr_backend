from ast import Str
import json
import os
from typing import Any
from unicodedata import name
from fastapi import Response, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select, delete, Column
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from sqlalchemy import asc, desc

from loguru import logger
from pydantic import Json
# from rich import print
from apps.repositories.repo_service import DB_Service

from config import settings
from apps.db import Base
from apps.repositories.repo_uow import UnitOfWork
from apps.repositories.repo_SQL import SQLRepo
from apps.schemas.file_data import Schema_file_data_ID, Schema_file_delete_out, Schema_pdf, Schema_upload_pdf
from apps.models import models_clases
from utils.funcs import save_file, delete_file
from apps.schemas.__dynamic_model import AutoSchema
from apps.models._base._info import Info
from apps.models.references.doc_type import Doc_type
from apps.models._base.doc_file import Doc_file

from apps.schemas.general import Schema_General
from apps.schemas.__basemodel import Base_Model


class DB_Service_extra:

    @staticmethod
    def async_with_uow(func):
        '''Декоратор для контекстного менеджера'''
        # @cache(expire=30)
        async def wrapper(uow, *args, **kwargs):
            async with uow:
                return await func(uow, *args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    @staticmethod
    async def get_tables_columns():
        '''Получаем все колонки всех таблиц'''
        models: list[Base] = models_clases
        def funforeignKeyTable(column: Column):
            if len(column.foreign_keys) != 0:
                return list(column.foreign_keys)[0].column.table.name
            else:
                return None
        def to_dict(column: Column): 
            return dict(
                name = column.key,
                type = column.type._type_affinity.__name__.lower(),
                label = column.comment,
                foreign_key = funforeignKeyTable(column),
                primary_key = column.primary_key
            )
        return {model.__tablename__: [to_dict(column) for column in model.__table__.columns] for model in models}


    @staticmethod
    @async_with_uow
    async def get_tables_rows(uow: UnitOfWork, models: list[Base], schema_tables_rows_out_keys: list[str]):
        '''Получаем все строки всех таблиц'''
        allrows = {}
        models = [model for model in models if model.__tablename__ in schema_tables_rows_out_keys]
        for model in models:
            # query = select(model)
            query = select(model).order_by(asc(model.__table__.primary_key.columns))
            result = await uow.session.scalars(query)
            rows =  result.unique().all()
            # allrows[model.__tablename__] = [model.convert_model_to_dict(row) for row in rows]
            allrows[model.__tablename__] = [model.enhanced_convert(row) for row in rows]
        return allrows
    

    @staticmethod
    async def get_patch_file(uow: UnitOfWork, data: Schema_upload_pdf):
        print(data)
        # model_info: SQLRepo = getattr(uow, 'info')
        # result_info = await model_info.session.get(Info, data.info_id)
        # catalog = result_info.catalog

        model_doc_type: SQLRepo = getattr(uow, 'doc_type')
        result_model_doc_type = await model_doc_type.session.get(Doc_type, data.doc_type_id)
        result_model_doc_type_name = result_model_doc_type.name.replace('/', '_')
        doc_type_name = f"{data.info_id}.{data.doc_type_id}. {result_model_doc_type_name}.pdf"

        # patch = f"{settings.ROOT_DIRECTORY_OF_DOCUMENTS}\\{catalog}\\{doc_type_name}"
        patch = f"{settings.ROOT_DIRECTORY_OF_DOCUMENTS}\\{data.info_id}\\{doc_type_name}"
        return patch, doc_type_name


    @staticmethod
    @async_with_uow
    async def upload_pdf(uow: UnitOfWork, data: Schema_upload_pdf, file: UploadFile):
        if file.content_type == 'application/pdf':
            patch, file.filename = await __class__.get_patch_file(uow, data)
            data: dict = data.model_dump()
            data["name"] = file.filename
            data = {k: v for k, v in data.items() if v != None}
            print("data = ", data)
            model_doc_file: SQLRepo = getattr(uow, 'doc_file')
            rows = await model_doc_file.upsert(data)
            result: list[Base] = [model_doc_file.model.convert_model_to_dict(row) for row in rows]
            save_file(patch, file)
            await uow.commit()
            return Response(status_code=200, content = json.dumps(result[0]))
            # return Response(status_code=200, content=f"Документ: {file.filename} - загружен в архив")
        else:
            return Response(status_code=200, content=f"Загружаемый файл {file.filename}, должен быть в формате PDF")        


    @staticmethod
    async def doc_file_relation(uow: UnitOfWork):
        model = Doc_file
        query = (
            select(model)
            .options(joinedload(model.doc_type))
            .options(joinedload(model.info))
        )
        res = await uow.session.execute(query)
        models = res.unique().scalars().all()        
        return [model.result_models_to_read(Schema_pdf) for model in models]


    @staticmethod
    @async_with_uow
    async def download_file(uow: UnitOfWork, id: int |str):
        '''Скачивает файл в браузер пользователю'''
        print(id, type(id))
        model = Doc_file
        query = (
            select(model).filter_by(id = id)
            .options(joinedload(model.info))
        )
        model = await uow.session.scalar(query)
        # models = res.unique().scalars().all()        
        res: Schema_pdf =  model.result_models_to_read(Schema_pdf)
        # res: Schema_pdf =  Schema_pdf.model_validate(model)
        # catalog = res['catalog']
        catalog = res['info_id']
        filename = res['name']
        path = f"{settings.ROOT_DIRECTORY_OF_DOCUMENTS}\\{catalog}\\{filename}"
        print(f"'{path}'")
        headers = {'Content-Disposition': 'inline'}
        if os.path.isfile(path):
            return FileResponse(
                status_code = 200,
                path = path, 
                filename = filename, 
                media_type = 'application/pdf',
                # headers = headers,
                # content_disposition_type = "attachment",
                # content_disposition_type = "inline",
                # media_type = 'multipart/form-data',
            )
        else:
            return Response(status_code=200, content = f"Файл {filename}: отсутствует...".encode())


    @staticmethod
    @async_with_uow
    async def deleted_file_pdf(uow: UnitOfWork, data: Any):
        '''Удаляем файлы из каталога и из базы данных'''
        rows = await __class__.doc_file_relation(uow)
        if rows:
            logger.warning(f"{data = }")
            filter_data = list(filter(lambda row: row["id"] in data, rows))
            print({f"{filter_data = }"})
            for i in filter_data:
                await uow.session.execute(delete(Doc_file).filter_by(name = i["name"]))
                xxx = delete_file(f"{settings.ROOT_DIRECTORY_OF_DOCUMENTS}\\{i['info_id']}\\{i['name']}")
                if xxx == True: 
                    await uow.session.flush()
                    logger.success(f"Файл {i['name']} удален")
                else:
                    logger.error(f"Файл {i['name']} для удаления не найден")
                    return f"Файл {i['name']} для удаления не найден"
            await uow.commit()
            return [Schema_file_delete_out.model_validate(model).model_dump() for model in filter_data]


    @staticmethod
    @async_with_uow
    async def update(uow: UnitOfWork, data: Any):
        '''Обновляем базы данных'''
        print(data)
        service: SQLRepo = getattr(uow, data['name'])
        # await service.upsert(data['value'])

        await service.update_list(data['value'])
        await uow.commit()
        print("'Данные обновлены ...'")
        return json.dumps(data, indent=2)
        # return data



    @staticmethod
    @async_with_uow
    async def send_data(uow: UnitOfWork, data: Any):
        '''Удаляем файлы из каталога и из базы данных'''
        # print(data)
        service: SQLRepo = getattr(uow, data['name'])
        use_schema: AutoSchema = AutoSchema(service.model)
        value: dict = data['value']

        update_data = value.get('update_data', [])
        delete_data = value.get('delete_data', [])
        temp_add_data = value.get('add_data', [])

        # print("use_schema.IN.__annotations__ = ", use_schema.IN.__annotations__)

        if len(temp_add_data) != 0:
            add_data = [use_schema.IN.model_validate(row).model_dump() for row in temp_add_data]
            print(f"{add_data = }")
            await service.add_list(add_data)
            await uow.session.flush()

        if len(update_data) != 0:
            print(f"{update_data = }")
            await service.update_list(update_data)
            await uow.session.flush()
        
        if len(delete_data) != 0:
            print(f"{delete_data = }")
            await service.delete_list_dict(delete_data)
            await uow.session.flush()
        
        new_data = await service.get_all_rows()
        new = [service.model.convert_model_to_dict(row) for row in new_data] 
        await uow.commit()
        print(new)
        return new



        # return json.dumps(new, indent=2)



        # print(add_data)
        # print(update_data)


        # await service.upsert(data['value'])

        # await service.update_list(data['value'])
        # # await uow.commit()
        # print("'Данные обновлены ...'")
        # return json.dumps(data, indent=2)
        # return data


    @staticmethod
    @async_with_uow
    async def get_one_table_rows(uow: UnitOfWork, table_name: str):
        '''Получаем все строки одной таблицы'''
        uow_attr: SQLRepo = getattr(uow, table_name)
        rows = await uow_attr.get_all_rows()
        new = [uow_attr.model.convert_model_to_dict(row) for row in rows] 
        print(f"___{new = }")
        # return json.dumps(new, indent=2)
        return new
    


