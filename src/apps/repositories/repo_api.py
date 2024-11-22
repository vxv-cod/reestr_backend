import asyncio
from datetime import date
import json
import os
from typing import Any, Annotated, Optional, Union
from fastapi import APIRouter, Depends, UploadFile, Response
from fastapi.responses import FileResponse
from pydantic import Field, ValidationError, create_model, Json
from sqlalchemy import Column, Inspector, select
from sqlalchemy.engine import Connection
from sqlalchemy.inspection import inspect
# from rich import print
from loguru import logger

from fastapi import Form
from fastapi import File

from apps.db import Base, async_engine
from apps.dependencies.dep_uow import DataBase_depend_UOW
# from apps.models._base import doc_file
from apps.repositories.repo_service import DB_Service
from apps.repositories.repo_service_extra import DB_Service_extra
from apps.schemas.file_data import Schema_file_delete_list, Schema_file_data, Schema_file_data_ID, Schema_file_delete
from apps.schemas.file_data import Schema_upload_pdf
from apps.schemas.__basemodel import Base_Model
from apps.schemas.__dynamic_model import AutoSchema
from apps.schemas.__depends import dep_file_data, dep_upload_pdf, dep_UploadFile
from config import settings
from apps.models import models_clases
from apps.repositories.repo_uow import UnitOfWork

# dep_models_clases = Annotated[list[Base], models_clases]
class Api_Base:

    def __init__(self, model_orm: Base):
        self.model: Base = model_orm
        self.tablename = self.model.__tablename__
        self.tags = [self.tablename]
        self.router = APIRouter(prefix = f"/{self.tablename}", tags=self.tags)
        self.service = DB_Service(self.tablename)
        self.use_schema: AutoSchema = AutoSchema(self.model)


    def dto(self, data: list[Base_Model] | Base_Model):
        if isinstance(data, list):
            return [i.model_dump() for i in data]
        else:
            return data.model_dump()
        

class Api_default(Api_Base):

    def __init__(self, model_orm):
        super().__init__(model_orm)
        

        @self.router.get("/get_all", response_model = list[self.use_schema.ALL])
        async def get_all(uow: DataBase_depend_UOW):
            return await self.service.get_all_rows(uow, self.use_schema.ALL)


        @self.router.get("/get_one", response_model = self.use_schema.ALL)
        async def get_one(uow: DataBase_depend_UOW, ids: self.use_schema.PK_only):
            return await self.service.get_one_by_multi_id(uow, ids, self.use_schema.ALL)


        @self.router.post("/add_one", response_model = self.use_schema.ALL)
        async def add_one(uow: DataBase_depend_UOW, data: self.use_schema.IN):
            return await self.service.add_one(uow, data)

       
        @self.router.post("/upsert", response_model = list[self.use_schema.ALL])
        async def upsert(uow: DataBase_depend_UOW, data: list[self.use_schema.ALL]):
            '''Добавляем объекты, если нет и обновляем, если есть'''
            return await self.service.upsert(uow, self.dto(data), self.use_schema.ALL)


        @self.router.delete("/delete_list")
        async def delete_list(uow: DataBase_depend_UOW, data: list[int]):
            return await self.service.delete_list(uow, data)


        '''Связи ... '''
        # @self.router.get("/get_all_relation_true", 
        #     include_in_schema = self.use_schema.include_in_schema(), 
        #     response_model = list[self.use_schema.ALL_i_REL]
        # )
        # async def get_all_relation_true(uow: DataBase_depend_UOW):
        #     return await self.service.get_all_rows(uow, self.use_schema.ALL_i_REL)
        

        # @self.router.get("/get_one_relation_true", 
        #     include_in_schema = self.use_schema.include_in_schema(), 
        #     response_model = self.use_schema.ALL_i_REL)
        # async def get_one_relation_true(uow: DataBase_depend_UOW, ids: self.use_schema.PK_only):
        #     return await self.service.get_one_by_multi_id(uow, ids, self.use_schema.ALL_i_REL)

from pydantic import BaseModel, Json


class Api_frontend_store:

    @staticmethod
    def schema_tables_rows():
        models: list[Base] = models_clases
        # models = [model for model in models if model.__tablename__ not in ['phonebook', 'business_process']]
        type_value = lambda model=Base: AutoSchema(model).pydantic_dynamic_model(model)
        # type_value = lambda model=Base: AutoSchema(model).pydantic_dynamic_model(model, text="ALL_i_REL", relation=True)
        schema = {model.__tablename__: Annotated[type_value(model) | list[type_value(model)] | None, Field(...)] for model in models}
        return create_model("name_new_cls", **schema)
    

    def __init__(self, tags: str):
        # self.tablename = tablename
        self.tags = [tags]
        self.router = APIRouter(prefix = f"/{tags}", tags=self.tags)
        self.dep_models_clases = Annotated[list[Base], Depends(lambda : models_clases)]
        self.schema_tables_rows_out: Base_Model = self.schema_tables_rows()
        self.schema_tables_rows_out_keys: list[str] = self.schema_tables_rows_out.model_fields.keys()


        @self.router.get("/get_tables_columns")
        async def get_tables_columns():
            '''Получаем все колонки всех таблиц'''
            return await DB_Service_extra.get_tables_columns()


        @self.router.get("/get_tables_rows", response_model = self.schema_tables_rows_out)
        async def get_tables_rows(uow: DataBase_depend_UOW, models: self.dep_models_clases):
            '''Получаем все строки всех таблиц'''
            return await DB_Service_extra.get_tables_rows(uow, models, self.schema_tables_rows_out_keys)


        @self.router.post("/upload_pdf")
        async def upload_pdf(uow: DataBase_depend_UOW, data: dep_upload_pdf, file: dep_UploadFile):
            return await DB_Service_extra.upload_pdf(uow, data, file)

       
        @self.router.post("/download_file")
        async def download_file(uow: DataBase_depend_UOW, id: Annotated[Json, Form(...)]):
            return await DB_Service_extra.download_file(uow, id)


        @self.router.delete("/deleted_file_pdf")
        async def deleted_file_pdf(uow: DataBase_depend_UOW, data: Annotated[Json, Form(...)]):
            return await DB_Service_extra.deleted_file_pdf(uow, data)

       
        # @self.router.post("/upsert")
        @self.router.post("/update")
        async def update(uow: DataBase_depend_UOW, data: Annotated[Json, Form(...)]):
            '''Добавляем объекты, если нет и обновляем, если есть'''
            return await DB_Service_extra.update(uow, data)


        @self.router.post("/send_data")
        async def send_data(uow: DataBase_depend_UOW, data: Annotated[Json, Form(...)]):
            '''Добавляем объекты, если нет и обновляем, если есть'''
            return await DB_Service_extra.send_data(uow, data)




        @self.router.get("/get_one_table_rows")
        async def get_one_table_rows(uow: DataBase_depend_UOW, table_name: str):
            print(f'{table_name = }')
            '''Получаем все строки одной таблицы'''
            return await DB_Service_extra.get_one_table_rows(uow, table_name)

        
        # async def get_one_table_rows(uow: DataBase_depend_UOW, table_name: str):
        #     '''Получаем все строки одной таблицы'''
        #     return await DB_Service_extra.get_one_table_rows(uow, table_name)





        # @self.router.post("/upload_pdf")
        # async def upload_pdf(uow: DataBase_depend_UOW, 
        #     data: Schema_upload_pdf = Form(...), 
        #     file: UploadFile = File(...)
        # ):
        #     logger.debug(f"{data = }")
        #     print(f"{file = }")
        #     return "Test ..."



        # @self.router.post("/upload_pdf_test")
        # async def upload_pdf_test(uow: DataBase_depend_UOW, 
        #     # data: Json[Schema_upload_pdf] | Json = Form(...), 
        #     # file: UploadFile = File(...)
            
        #     # data: Json[Schema_upload_pdf] | Schema_upload_pdf = Form(...), 
        #     # file: UploadFile | None = File(...), 
            
        #     data: Schema_upload_pdf_test_222 = Form(...), 
        #     file: UploadFile= File(...), 
            
        #     # id: int = Form(),
        #     # info_id: int = Form(),
        #     # doc_type_id: int  = Form(),
        #     # file: UploadFile = Form(...)            
        #     ):
        #     # logger.debug(f"{id = }")
        #     # logger.debug(f"{info_id = }")
        #     # logger.debug(f"{doc_type_id = }")

        #     logger.debug(f"{data = }")
        #     logger.debug(f"{type(data) = }")
        #     logger.debug(f"{data.model_dump() = }")
        #     logger.debug(f"{file.filename = }")
        #     # data = json.loads(data)

        #     # xxx = Schema_upload_pdf_test_222.model_validate_json(data)
        #     # logger.debug(f"{xxx = }")
        #     # "{\"id\":null,\"info_id\":1,\"doc_type_id\":3}"
        #     # "\"data\" = {\"id\":null,\"info_id\":1,\"doc_type_id\":3}" 
            
        #     # print(f"{file = }")
        #     return "Test ..."
        
        
        # @self.router.post("/upload_pdf_test")
        # async def upload_pdf_test(uow: DataBase_depend_UOW, 
        #     data: Schema_upload_pdf = Form(...), 
        #     file: UploadFile = File(...)
        # ):
        #     # data = json.loads(data)

        #     # xxx = Schema_upload_pdf_test_222.model_validate_json(data)
        #     # logger.debug(f"{xxx = }")
        #     # "{\"id\":null,\"info_id\":1,\"doc_type_id\":3}"
        #     # "\"data\" = {\"id\":null,\"info_id\":1,\"doc_type_id\":3}" 
            
        #     # print(f"{file = }")
        #     return "Test ..."








        # @self.router.post("/upload_pdf_test")
        # async def upload_pdf_test(id : int = Form(...), info_id: int = Form(...), doc_type_id: int = Form(...) ):
        #     print(f"{id = }")
        #     return "upload_pdf_test ..."

        
        # @self.router.post("/upload_pdf_test")
        # async def upload_pdf_test(
        #     id : int = Form(...), 
        #     info_id: int = Form(...), 
        #     doc_type_id: int = Form(...)

        #     ):
        #     print(f"{id = }")
        #     return "upload_pdf_test ..."


        # @self.router.post("/upload_pdf")
        # # async def upload_pdf(uow: DataBase_depend_UOW, data: Schema_file_data_ID, file: UploadFile,):
        # async def upload_pdf(
        #     data : Annotated[Schema_upload_pdf,  Depends()],
        #     file: UploadFile,
        #     ):

        #     print(f"{file = }")
        #     print(f"{data = }")
        #     return "Test ..."
        




        # @self.router.post("/form")
        # async def form_post(form_data: SimpleModel = Depends()):
        #     fp = await form_data.f.read()
        #     print(fp)




        # @self.router.get("/download_file")
        # async def download_file(filename: str, catalog: str):
        #     '''Скачивает файл в браузер пользователю'''
        #     return await DB_Service_extra.download_file(filename, catalog)

            

        # @self.router.delete("/delete_file")
        # # async def delete_file(uow: DataBase_depend_UOW, data: Schema_file_delete_list):
        # async def delete_file(uow: DataBase_depend_UOW, data: Schema_file_delete):
        #     data = data.model_dump()
        #     print(data)
        #     return data



'''
class Api_doc_file_options(Api_Base):
    def __init__(self, model_orm):
        super().__init__(model_orm)
        @self.router.get("/download_file")
        async def download_file(filename: str, catalog: str):
            path = f"{settings.ROOT_DIRECTORY_OF_DOCUMENTS}\\{catalog}\\{filename}"
            if os.path.isfile(path):
                return FileResponse(
                    status_code = 200,
                    path = path, content_disposition_type = "attachment",
                    filename = filename, media_type = 'multipart/form-data',
                )
            else:
                return Response(status_code=200, content = f"Файл {filename}: отсутствует...".encode())
        @self.router.delete("/delete_file")
        async def delete_file(uow: DataBase_depend_UOW, data: Schema_file_delete_list):
            data = data.model_dump()
            print(data)
            return data

# @self.router.get("/get_tables_columns")
# async def get_tables_columns():
#     async with async_engine.connect() as conn:
#         res = await conn.run_sync(self.euse_inspector_multi_columns)
#         return res
'''

''' Вариант с inspect
@staticmethod
def euse_inspector_multi_columns(conn: Connection):
    insp = inspect(conn)
    res_dict = {}
    multi_columns = insp.get_multi_columns()
    for (schema, table_name), columns in multi_columns.items():
        if table_name != "alembic_version":
            res = []
            for column in columns:
                obj = {}
                obj['name'] = column["name"]
                obj["type"] = column["type"]._type_affinity.__name__
                obj['label'] = column.get('comment', None)
                res.append(obj)
            res_dict[table_name] = res
    return res_dict
'''     


            

        # @self.router.post("/filter_by_list", tags=self.tags)
        # async def filter_by_list(uow: DataBase_depend_UOW, items: list[int | str]) -> list[self.db_schema_out]:
        #     '''Получаем не все объекты, а только те, которые укажем в списке из id нужных объектов'''
        #     return await self.service.filter_by_list(uow, items)

        
        # @self.router.get("/get_all", tags=self.tags, response_model = list[self.db_schema_out], include_in_schema=False)
        # async def get_all(uow: DataBase_depend_UOW):
        #     '''Получаем все объекты'''
        #     return await self.service.get_all(uow)


        # def use_inspector(conn: Connection, table, res = []):
        #     '''Получаем данные из таблиыц (имя, тип колонки, комментарий)'''
        #     insp = inspect(conn)
        #     insp_columns = insp.get_columns(table_name = table)
        #     for column in insp_columns:
        #         obj = {}
        #         obj['name'] = column['name']
        #         obj["type"] = column['type']._type_affinity.__name__
        #         obj['label'] = column['comment']
        #         res.append(obj)
        #     return res


        # @self.router.get("/get_headers", tags=self.tags)
        # async def get_headers():
        #     logger.debug(self.tags)
        #     table = self.tags[0]
        #     async with async_engine.connect() as conn:
        #         res = await conn.run_sync(use_inspector, table)
        #         return res


        # @self.router.get("/get_table", tags=self.tags)
        # async def get_table(uow: DataBase_depend_UOW):
        #     columns = await get_headers()
        #     async with uow:
        #         rows = await get_all_relation_none(uow)
        #     return {"columns": columns, "rows": rows}

    

#         @self.router.get("/get_items_filter_by_users_zgd", tags=self.tags)
#         # @cache(expire=30)
#         async def get_items_filter_by_users_zgd(uow: DataBase_depend_UOW):
#             data = await self.service.get_all_filter(uow, filter_table_name = "user_zgd", model_col = "pk_name")
#             return {"count": len(data), "data": data}
    

#         @self.router.get("/get_items_filter_by_users_zgd_only_id", tags=self.tags)
#         # @cache(expire=30)
#         async def get_items_filter_by_users_zgd_only_id(uow: DataBase_depend_UOW):
#             data = await get_items_filter_by_users_zgd(uow)
#             data = [i["id"] for i in data["data"]]
#             return {"count": len(data), "data": data}











            

# class Api_DB_user_zgd(Api_default):
#     def __init__(self, prefix, tags, api_model):
#         super().__init__(prefix, tags, api_model)


#         @self.router.post("/upload_file_xlsx", tags=self.tags)
#         async def upload_file_xlsx(
#             uow: DataBase_depend_UOW, 
#             file: Annotated[bytes, File()],
#             background_tasks: BackgroundTasks,
#         ):
#             # background_tasks.add_task(self.service.upload_data_from_xlsx, uow, file, function=load_zgd)
#             # return "Задачи выполняются в фоне"
#             return await self.service.upload_data_from_xlsx(uow, file, load_zgd)


#         @self.router.get("/download_file_xlsx", tags=self.tags)
#         async def download_file_xlsx(filename: str):
#             some_file_path = f'src/store/{filename}'
#             headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
#             return FileResponse(path=some_file_path, headers=headers)






        # def enhanced_obj_to_dict(obj):
        #     '''### Итерация по ассоциациям — relationships! 🥳'''
        #     data = obj_to_dict(obj)
        #     inspect_manager = inspect(obj.__class__)
        #     relationships = inspect_manager.relationships
        #     for rel in relationships:
        #         if rel.lazy != "select":
        #             value = getattr(obj, rel.key)
        #             if isinstance(value, list):
        #                 data[rel.key] = [obj_to_dict(child).get("name", obj_to_dict(child)) for child in value]
        #             else:
        #                 data[rel.key] = sorted(obj_to_dict(value).get("name", obj_to_dict(value)) if value else None)
        #     return data























        # @self.router.post("/upload_file_xlsx_test", tags=self.tags)
        # async def upload_file_xlsx_test(
        #     uow: DataBase_depend_UOW, 
        #     file: Annotated[bytes, File()],
        #     background_tasks: BackgroundTasks, 
        # ):
        #     # return await self.service.save_in_db(uow, load_zgd(io.BytesIO(file)))

        #     background_tasks.add_task(self.service.save_in_db, uow, load_zgd(io.BytesIO(file)))
        #     return "Задачи выполняются в фоне"







        # @self.router.post("/upload_file_xlsx_test", tags=self.tags)
        # async def upload_file_xlsx_test(uow: DataBase_depend_UOW, file: Annotated[bytes, File()]):
            # import tempfile
            # with tempfile.NamedTemporaryFile(mode="w+b", suffix=".xlsx", delete=False) as temp_file:
            #     temp_file.write(file)            
            #     data = load_zgd(temp_file)
            # return await self.service.save_in_db(uow, data)








            # print(UploadFile.file.read())
            # buffer = io.BytesIO()
            # with UploadFile.file as temp_file:
            #     temp_file.write(buffer.getvalue())
            #     print(f"{buffer.getvalue()}")
            # xxx = load_zgd(temp_file.name)
            # print(xxx)

            # load_zgd(UploadFile.file.name)
            
            # temp_file.write(buffer.getvalue())
            # buffer = io.BytesIO()
            # file.file(mode="w+b", suffix=".xlsx", delete=False)
            # file.write(buffer.getvalue())
            # print(UploadFile.__dict__)
            # xxx = load_zgd(UploadFile.file)
            # print(xxx)
            

            # return "dddddd"


            # return await self.service.save_in_db(uow, UploadFile.file.name)



            # await file.SpooledTemporaryFile
            # buffer = io.BytesIO()
            # '''Сохранение документа в буфер обмена'''
            # # file.save(buffer)
            # buffer.seek(0)

            # data = load_zgd(buffer)
            # return data
            # return await self.service.save_in_db(uow, data)
        




        # async def add_from_xlsx(uow: DataBase_depend_UOW, data: load_zgd = Depends()):
        # async def add_from_xlsx(uow: DataBase_depend_UOW, file: Annotated[UploadFile, File()]):
        # async def add_from_xlsx(uow: DataBase_depend_UOW, file: UploadFile):
        #     print(f"{file.headers = }")
        #     print(f"{file.content_type = }")
        #     print(f"{file.content_type = }")

        #     xxx = load_zgd(file)
        #     # print(f"{await file.read() = }")
        #     return {"filename": file.filename}







        
        
        # @self.router.delete("/delete_list", tags=self.tags)
        # async def delete_list(uow: DataBase_depend_UOW, data: list[int]):
        #     return await self.service.delete_list(uow, data)
        

        # @self.router.get("/get_all_id")
        # async def get_all_id(uow: DataBase_depend_UOW):
        #     return await self.service.get_all_id(uow)


        # @self.router.post("/add_one")
        # async def add_one(uow: DataBase_depend_UOW, data: self.db_schema):
        #     return await self.service.add_one(uow, data.model_dump())


        # @self.router.post("/add_list", tags=self.tags)
        # async def add_list(uow: DataBase_depend_UOW, data: list[self.db_schema]):
        #     return await self.service.add_list(uow, [row.model_dump() for row in data])


        # @self.router.put("/update_one")
        # async def update_one(uow: DataBase_depend_UOW, data: self.db_schema):
        #     return await self.service.update_one(uow, data.model_dump())


        # @self.router.put("/update_list", tags=self.tags)
        # async def update_list(uow: DataBase_depend_UOW, data: list[self.db_schema]):
        #     return await self.service.update_list(uow, self.dto(data))


        
            # primary_keys = [key.name for key in value.target.primary_key]
            # convert = lambda x: {k:i for k, i in x.__dict__.items() if isinstance(i, Union[str, int, list])}
            # convert = lambda x: {k:i for k, i in x.__dict__.items() if k in primary_keys}
            # convert = lambda x = Base: {c.key: getattr(x, c.key) for c in inspect(x).mapper.column_attrs if c.key in x.primary_key}
            
            # convert = lambda x = Base: {c.key: getattr(x, c.key) for c in inspect(x).mapper.column_attrs for r in c.columns if r.primary_key}
        

        # def convert_model_to_dict(value, primary_key_only=False):
        #     from sqlalchemy.sql.schema import Column

        #     def safe_convert(data_type, value):
        #         try:
        #             return data_type(value)
        #         except (ValueError, TypeError):
        #             return None
        #     # row_dict = lambda column = Column: {column.name: safe_convert(column.type.python_type, getattr(model, column.name))}
            
        #     def convert(model: Base, row_dict = {}):
        #         columns: list[Column] = model.__table__.columns
        #         for column in columns:
        #             # action = safe_convert(column.type.python_type, getattr(model, column.name))
        #             action = getattr(model, column.name)
        #             if primary_key_only:
        #                 if column.primary_key:
        #                     row_dict[column.name] = action
        #                 else:
        #                     continue
        #             else:
        #                 row_dict[column.name] = action

        #         return row_dict
                
        #     # row_dict = {col.name: safe_convert(col.type.python_type, getattr(model, col.name)) for col in columns}
        #     # print(res)

        #     if isinstance(value, list):
        #         return [convert(child) for child in value]
        #     else:
        #         return convert(value)if value else None        
            

# class Api_doc_file_options(Api_Base):

    # def __init__(self, tags: str):
    #     self.tags = [tags]
    #     self.router = APIRouter(prefix = f"/{tags}")


        # @self.router.post("/upload_pdf", tags=self.tags)
        # async def upload_pdf(data: dep_file_data, file: UploadFile, uow: DataBase_depend_UOW):
        #     from apps.models._base._info import Info
        #     if file.content_type == 'application/pdf':
        #         async with uow:
        #             result = await uow.session.get(Info, data.info_id)
        #             catalog = result.catalog
        #             patch = f"{settings.ROOT_DIRECTORY_OF_DOCUMENTS}\\{catalog}\\{file.filename}"
        #             data = data.model_dump()
        #             data["patch"] = patch

        #             '''Ищем запись о файле с искомым полным именем (patch)'''
        #             query_find_file = select(Doc_file).filter_by(patch = patch)
        #             result_find_file = await uow.session.execute(query_find_file)
        #             find_file = result_find_file.scalar_one_or_none()
                    
        #             if find_file:
        #                 query = update(Doc_file).filter_by(id = find_file.id)
        #                 await uow.session.execute(query, data)
        #             else:
        #                 insert_query = insert(Doc_file)
        #                 await uow.session.execute(insert_query, data)
                    
        #             save_file(patch, file)
        #             await uow.commit()
        #         return Response(status_code=200, content=f"Документ: {file.filename} - загружен в архив")
        #     return Response(status_code=200, content=f"Загружаемый файл {file.filename}, должен быть в формате PDF")


                # query = (
                #     select(mod_cls)
                #     .options(joinedload(mod_cls.doc_file).joinedload(Doc_file.doc_type))
                # )

                # result = await uow.session.scalars(query)
                # models: list[Base] = result.unique().all()