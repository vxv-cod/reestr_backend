import io
import os
import sys
from typing import Any, Type, Union
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger
from openpyxl import load_workbook
from rich import print
from fastapi_cache.decorator import cache
from sqlalchemy.engine import Connection
# from sqlalchemy import inspect, select
from sqlalchemy import select
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.relationships import _RelationshipDeclared
from sqlalchemy.sql.schema import Column


from apps.db import Base
from apps.dependencies.dep_uow import DataBase_depend_UOW
# from apps.models.sensors import Sensors, TypeSensor
from apps.repositories.repo_service import DB_Service
from apps.schemas.__basemodel import Base_Model
from apps.schemas.save_in_db import Schema_save
from apps.db import async_engine





class Api_Base:
    
    def sqlresult_in_py(self, data: list[Base_Model] | Base_Model):
        if isinstance(data, list):
            return [i.model_dump() for i in data]
        if isinstance(data, Base_Model):
            return data.model_dump()


    def __init__(self, attr_uow_name, db_shama_in, db_shama_out, typeid):
        self.tags = [attr_uow_name]
        self.db_shama_in = db_shama_in
        self.db_shama_out = db_shama_out
        self.router = APIRouter(prefix = f"/{attr_uow_name}")
        self.service = DB_Service(attr_uow_name)
        self.typeid = typeid


class Api_inspect:
    def __init__(self, attr_uow_name):
        self.tags = [attr_uow_name]
        self.router = APIRouter(prefix = f"/{attr_uow_name}")        

        def euse_inspector_multi_columns(conn: Connection):
            insp = inspect(conn)
            res_dict = {}
            multi_columns = insp.get_multi_columns()
            for (schema, table_name), columns in multi_columns.items():
                if table_name != "alembic_version":
                    res = []
                    for column in columns:
                        obj = {}
                        obj['name'] = column.get('name', None)
                        type_field = column.get('type', None)
                        obj["type"] = type_field.python_type.__name__ if type_field else type_field
                        obj['label'] = column.get('comment', None)
                        res.append(obj)
                    res_dict[table_name] = res
            return res_dict

        @self.router.get("/get_multi_columns", tags=self.tags)
        async def get_multi_columns():
            async with async_engine.connect() as conn:
                res = await conn.run_sync(euse_inspector_multi_columns)
                return res


class Api_default(Api_Base):
    def __init__(self, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(attr_uow_name, db_shama_in, db_shama_out, typeid)


        @self.router.post("/add_one", tags=self.tags, response_model = self.db_shama_out)
        async def add_one(uow: DataBase_depend_UOW, data: self.db_shama_in):
            return await self.service.add_one(uow, data.model_dump())


        # @self.router.get("/get_all", tags=self.tags, response_model = list[self.db_shama_out])
        # async def get_all(uow: DataBase_depend_UOW):
        #     '''Получаем все объекты'''
        #     return await self.service.get_all(uow)
        


        def use_inspector(conn: Connection, table, res = []):
            '''Получаем данные из таблиыц (имя, тип колонки, комментарий)'''
            insp = inspect(conn)
            insp_columns = insp.get_columns(table_name = table)
            for column in insp_columns:
                obj = {}
                obj['name'] = column['name']
                obj["dataType"] = column['type'].python_type.__name__
                obj['label'] = column['comment']
                res.append(obj)
            return res




        @self.router.get("/get_headers", tags=self.tags)
        async def get_headers():
            table = self.tags[0]
            
            async with async_engine.connect() as conn:
                res = await conn.run_sync(use_inspector, table)
                return res
            

        @self.router.get("/get_table", tags=self.tags)
        async def get_table(uow: DataBase_depend_UOW):
            columns = await get_headers()
            async with uow:
                rows  = await self.service.get_all(uow)
            return {"columns": columns, "rows": rows}





        def obj_to_dict(value):
            '''### Создаем словарь просто и безупречно 🚀'''
            convert = lambda model = Base: {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}
            return [convert(child) for child in value] if isinstance(value, list) else convert(value) if value else None
        
        
        def enhanced_obj_to_dict(obj: Base):
            '''### Итерация по ассоциациям — relationships! 🥳'''
            data = obj_to_dict(obj)
            inspect_manager = inspect(obj.__class__)
            relationships: list[_RelationshipDeclared] = inspect_manager.relationships

            for rel in relationships:
                if rel.lazy != "select": data[rel.key] = obj_to_dict(getattr(obj, rel.key))
            return data
        


        def convert_model_to_dict_inspect_variant(value, primary_key_only=False):
            from sqlalchemy.orm.properties import ColumnProperty
            '''### Конвертируем из класса Base в dict через inspect🚀'''
            def convert(model: Base, res = {}):
                column_attrs: list[ColumnProperty] = inspect(model).mapper.column_attrs
                for property in column_attrs:
                    for column in property.columns:
                        if primary_key_only and not column.primary_key: continue
                        res[column.name] = getattr(model, column.name)
                return res
            return [convert(child) for child in value] if isinstance(value, list) else convert(value) if value else None            
                    

        def convert_model_to_dict(value, primary_key_only=False):
            '''Конвертируем из класса Base в dict'''
            def convert(model: Base, row_dict = {}):
                columns: list[Column] = model.__table__.columns
                for column in columns:
                    if primary_key_only and not column.primary_key: continue
                    row_dict[column.name] = getattr(model, column.name)
                return row_dict
            return [convert(child) for child in value] if isinstance(value, list) else convert(value) if value else None


        def primary_enhanced_obj_to_dict(obj: Base):
            '''### Итерация по ассоциациям — relationships! 🥳'''
            data = convert_model_to_dict(obj)
            inspect_manager = inspect(obj.__class__)
            relationships: list[_RelationshipDeclared] = inspect_manager.relationships
            for rel in relationships:
                if rel.lazy != "select": 
                    data[rel.key] = convert_model_to_dict(getattr(obj, rel.key), 1)
            return data



                    

        @self.router.get("/get_all_relation_none", tags=self.tags)
        async def get_all_relation_none(uow: DataBase_depend_UOW):
            async with uow:
                query = select(getattr(uow, attr_uow_name).model)
                result = await uow.session.scalars(query)
                models: list[Base] = result.unique().all()

                return [convert_model_to_dict(model) for model in models]


        @self.router.get("/get_all_relation_true", tags=self.tags)
        async def get_all_relation_true(uow: DataBase_depend_UOW):
            async with uow:
                query = select(getattr(uow, attr_uow_name).model)
                result = await uow.session.scalars(query)
                models = result.unique().all()
                
                return [enhanced_obj_to_dict(model) for model in models]


        @self.router.get("/get_all_relation_true_primary_key", tags=self.tags)
        async def get_all_relation_true_primary_key(uow: DataBase_depend_UOW):
            async with uow:
                query = select(getattr(uow, attr_uow_name).model)
                result = await uow.session.scalars(query)
                models = result.unique().all()

                return [primary_enhanced_obj_to_dict(model) for model in models]
            

                # for obj in result:
                #     data = obj_to_dict(obj)
                #     inspect_manager = inspect(obj.__class__)
                #     relationships = inspect_manager.relationships

                #     # Итерация по ассоциациям — сложнее, чем интереснейшие отношения! 🥳
                #     for rel in relationships:
                #         value = getattr(obj, rel.key)
                #         data[rel.key] = obj_to_dict(value) if value else None
                #         if isinstance(value, list):
                #             data[rel.key] = [obj_to_dict(child) for child in value]
                #         else:
                #             data[rel.key] = None
                #     return data











        @self.router.get("/get_one", tags=self.tags, response_model = self.db_shama_out)
        async def get_one(uow: DataBase_depend_UOW, id: self.typeid):
            '''Получаем один объект по id'''
            return await self.service.get_one(uow, id)


        @self.router.post("/filter_by_list", tags=self.tags)
        async def filter_by_list(uow: DataBase_depend_UOW, items: list[int | str]) -> list[self.db_shama_out]:
            '''Получаем не все объекты, а только те, которые укажем в списке из id нужных объектов'''
            return await self.service.filter_by_list(uow, items)


        @self.router.put("/save_in_db", tags=self.tags, response_model = Schema_save)
        async def save_in_db(uow: DataBase_depend_UOW, data: list[self.db_shama_out]):
            '''Добавляем объекты, если нет и обновляем, если есть'''
            return await self.service.save_in_db(uow, self.sqlresult_in_py(data))







# class Api_contacts(Api_default):
#     def __init__(self, attr_uow_name, db_shama_in, db_shama_out, typeid):
#         super().__init__(attr_uow_name, db_shama_in, db_shama_out, typeid)



# # class Api_DB_historydata(Api_default):
# class Api_DB_historydata(Api_Base):
#     def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
#         super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)



    

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










# class Api_DB_type_sensor(Api_default):
#     def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
#         super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)


#         # @self.router.put("/save_in_db", tags=self.tags, 
#         #                  response_model = Prtg_schema_import_in_DB_id_Int)
#         # async def save_in_db(uow: DataBase_depend_UOW, data: list[self.db_shama_in]):
#         #     return await self.service.save_in_db(uow, self.sqlresult_in_py(data))


#         @self.router.post("/default", tags=self.tags,
#                          response_model = Prtg_schema_import_in_DB_id_Int)
#         async def default(uow: DataBase_depend_UOW):
#             return await self.service.save_in_db(uow, self.default_data)
            

# class Api_DB_user_zgd(Api_default):
#     def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
#         super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)


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
        # async def add_one(uow: DataBase_depend_UOW, data: self.db_shama):
        #     return await self.service.add_one(uow, data.model_dump())


        # @self.router.post("/add_list", tags=self.tags)
        # async def add_list(uow: DataBase_depend_UOW, data: list[self.db_shama]):
        #     return await self.service.add_list(uow, [row.model_dump() for row in data])


        # @self.router.put("/update_one")
        # async def update_one(uow: DataBase_depend_UOW, data: self.db_shama):
        #     return await self.service.update_one(uow, data.model_dump())


        # @self.router.put("/update_list", tags=self.tags)
        # async def update_list(uow: DataBase_depend_UOW, data: list[self.db_shama]):
        #     return await self.service.update_list(uow, self.sqlresult_in_py(data))


        
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