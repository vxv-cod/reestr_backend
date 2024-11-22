import os
from fastapi import Response, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select, Column
from loguru import logger


from apps.db import Base
from apps.repositories.repo_uow import UnitOfWork
from apps.repositories.repo_SQL import SQLRepo
from apps.schemas.__basemodel import Base_Model
from apps.schemas.file_data import Schema_file_data_ID
from apps.models import models_clases
from apps.models._base._info import Info
from utils.funcs import save_file
from config import settings



class DB_Service:

    def __init__(self, attr_uow_name):
        self.attr_uow_name = attr_uow_name
    

    @staticmethod
    def async_with_uow(func):
        '''Декоратор для контекстного менеджера'''
        # @cache(expire=30)
        async def wrapper(self, uow, *args, **kwargs):
            async with uow:
                return await func(self, uow, *args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    

    def uow_attr(self, uow: UnitOfWork) -> SQLRepo:
        '''Нахождение значения атирибута по имени репозитория DataBase'''
        return getattr(uow, self.attr_uow_name)


    @async_with_uow
    async def get_all_rows(self, uow: UnitOfWork, shama: Base_Model):
        models: list[Base] = await self.uow_attr(uow).get_all_rows()
        return [model.result_models_to_read(shama) for model in models]


    @async_with_uow
    async def get_one_by_multi_id(self, uow, ids: Base_Model, shama: Base_Model):
        '''Получаем строку из таблиц по одиному или нескольким id'''
        model: Base = await self.uow_attr(uow).get_one_by_multi_id(ids.model_dump())
        return model.result_models_to_read(shama)


    @async_with_uow
    async def add_one(self, uow: UnitOfWork, data: Base_Model):
        """Добавление одной строки из объекта"""
        res = await self.uow_attr(uow).add_one([data.model_dump()])
        await uow.commit()
        return res


    @async_with_uow
    async def upsert(self, uow: UnitOfWork, data: list[dict], shama: Base_Model):
        '''Обновление или вставка строк только для PostgreSQL'''
        models: list[Base] = await self.uow_attr(uow).upsert(data)
        await uow.commit()
        return [model.result_models_to_read(shama) for model in models]


    @async_with_uow
    async def delete_list(self, uow: UnitOfWork, data: list[int]):
        '''Удаление строк из списка id строк'''
        res = await self.uow_attr(uow).delete_list(data)
        await uow.commit()
        return res
    


# }
#   "info_id": 0,
#   "doc_type_id": 0,
#   "date": "2024-08-21",
#   "nomer": "string",
#   "patch": "string",
#   "id": 0
# }


    # @async_with_uow
    # async def upload_pdf(self, uow: UnitOfWork, data: Schema_file_data_in, file: UploadFile):
    #     from apps.models._base._info import Info
    #     if file.content_type == 'application/pdf':
    #         model_info: SQLRepo = getattr(uow, 'info')
    #         result = await model_info.session.get(Info, data.info_id)
    #         catalog = result.catalog
    #         patch = f"{settings.ROOT_DIRECTORY_OF_DOCUMENTS}\\{catalog}\\{file.filename}"
    #         data = data.model_dump()
    #         data["patch"] = patch
    #         '''Ищем запись о файле с искомым полным именем (patch)'''
    #         find_file = await self.uow_attr(uow).find_one(**{'patch': patch})
    #         if find_file:
    #             data["id"] = find_file.id
    #         await self.uow_attr(uow).upsert(data)
    #         save_file(patch, file)
    #         await uow.commit()
    #         return Response(status_code=200, content=f"Документ: {file.filename} - загружен в архив")
    #     else:
    #         return Response(status_code=200, content=f"Загружаемый файл {file.filename}, должен быть в формате PDF")        



    # @async_with_uow
    # async def get_rows_tables(self, uow: UnitOfWork, models_clases: list[Base] = models_clases):
    #     allrows = {}
    #     for model in models_clases:
    #         query = select(model)
    #         result = await uow.session.scalars(query)
    #         rows =  result.unique().all()
    #     allrows[model.__tablename__] = [model.convert_model_to_dict(row) for row in rows]
    #     return allrows
    










    # @async_with_uow
    # async def get_one(self, uow: UnitOfWork, id: int | str):
    #     '''Получение одной строки по id'''
    #     return await self.uow_attr(uow).get_one(id)

    # @async_with_uow
    # async def get_all(self, uow: UnitOfWork):
    #     '''Получение всех строк'''
    #     return await self.uow_attr(uow).get_all()


    # @async_with_uow
    # async def get_all_id(self, uow: UnitOfWork):
    #     '''Получение всех строк'''
    #     return await self.uow_attr(uow).get_all_id()
        

    # @async_with_uow
    # async def filter_by_list(self, uow: UnitOfWork, data: list[int]):
    #     '''Получение строк из списка id строк'''
    #     return await self.uow_attr(uow).filter_by_list(data)


    # @async_with_uow
    # async def get_all_filter(self, uow: UnitOfWork, filter_table_name: str, model_col: str):
    #     table_id_list: SQLRepo = getattr(uow, filter_table_name)
    #     filter_list = await table_id_list.get_all_id()
    #     '''Получение строк из списка id строк'''
    #     repo = self.uow_attr(uow)
    #     model_col = getattr(repo.model, model_col)
    #     return await repo.get_all_filter(model_col, filter_list)



    # @async_with_uow
    # async def add_list(self, uow: UnitOfWork, data: list[dict]):
    #     '''Добавление строк из списка с объектами'''
    #     res = await self.uow_attr(uow).add_list(data)
    #     await uow.commit()
    #     return res            


    # @async_with_uow
    # async def replace_all(self, uow: UnitOfWork, data: list[dict]):
    #     '''Удаляем все строки таблицы и вставляем новые'''
    #     db_repo = self.uow_attr(uow)
    #     '''Удаляем все строки в таблице'''
    #     await db_repo.session.execute(delete(db_repo.model))
    #     await uow.session.flush()
    #     '''Добавление новых строк'''
    #     res = await db_repo.add_list(data)
    #     await uow.commit()
    #     return res            


    # @async_with_uow
    # async def update_one(self, uow: UnitOfWork, data: dict):
    #     '''Обновление одной строки'''
    #     res = await self.uow_attr(uow).update_one(data)
    #     await uow.commit()
    #     return res


    # @async_with_uow
    # async def update_list(self, uow: UnitOfWork, data: list[dict]):
    #     '''Обновление строк из списка'''
    #     res = await self.uow_attr(uow).update_list(data)
    #     await uow.commit()
    #     return res
    
    

    # @async_with_uow
    # async def save_in_db(self, uow: UnitOfWork, data: list[dict]):
    #     '''Обновление или вставка строк'''
    #     res = await self.uow_attr(uow).upsert(data)
    #     await uow.commit()
    #     return res

    
    # async def upload_data_from_xlsx(self, uow, file, function):
    #     '''Полчение файла от фронта, обработка данных по function и помещение данных в ДБ'''
    #     data = function(io.BytesIO(file))
        
    #     return await self.save_in_db(uow, data)





        # query_find_file = select(Doc_file).filter_by(patch = patch)
        # result_find_file = await uow.session.execute(query_find_file)
        # find_file = result_find_file.scalar_one_or_none()
        
        # if find_file:
        #     query = update(Doc_file).filter_by(id = find_file.id)
        #     await uow.session.execute(query, data)
        # else:
        #     insert_query = insert(Doc_file)
        #     await uow.session.execute(insert_query, data)
        
        # save_file(patch, file)
        # await uow.commit()
        ...