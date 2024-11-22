from typing import Annotated, Any, Union
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, ValidationError, create_model
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from apps.schemas.__basemodel import Base_Model_id, Base_Model
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm.relationships import _RelationshipDeclared
from sqlalchemy.orm.mapper import Mapper
# from rich import print

from config import settings




sync_engine = create_engine(url=settings.DATABASE_URL_SUNC)
# sync_engine.echo = True
sync_session_maker = sessionmaker(bind=sync_engine)

async_engine = create_async_engine(settings.DATABASE_URL_ASUNC)
# async_engine.echo = settings.DEBUG
# async_engine.echo = True
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


# class Base(AsyncAttrs, DeclarativeBase):
class Base(DeclarativeBase):
    '''Если указать схему, то ее нужно прописывать перед названием таблицы в колонках'''
    # __table_args__ = {"schema": "stack"}
    
    pydantic_schema : BaseModel = None
    pydantic_schema_id : BaseModel = None
    

    @staticmethod
    def validerrdecor(func):
        def wrapper(self, *args, **kwargs):
            try: 
                res = func(self, *args, **kwargs)
            except ValidationError as exc: 
                print(repr(exc.errors()[0]))
                erro = exc.errors()[0]
                res = {"type": erro["type"], "loc": erro["loc"]}
            return res
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper


    @validerrdecor
    def result_models_to_read(self, schema: Base_Model) -> Base_Model:
        '''Валидируем модель без поля id'''
        return schema.model_validate(self.__dict__, from_attributes=True).model_dump()
    

    @staticmethod
    def convert_model_to_dict(value, primary_key_only=False):
        '''### Конвертируем из класса Base в dict'''
        def convert(model: Base, row_dict = {}):
            columns: list[Column] = model.__table__.columns
            for column in columns:
                if primary_key_only and not column.primary_key: continue
                row_dict[column.name] = getattr(model, column.name)
            
            return row_dict
        return [convert(child) for child in value] if isinstance(value, list) else convert(value) if value else None


    def enhanced_convert(self, primary_key_only=False):
        '''### Итерация по ассоциациям — relationships! 🥳'''
        data = self.convert_model_to_dict(self)
        inspect_manager = inspect(self.__class__)
        relationships: list[_RelationshipDeclared] = inspect_manager.relationships
        for rel in relationships:
            if rel.lazy != "select":
                data[rel.key] = self.convert_model_to_dict(getattr(self, rel.key), primary_key_only)
        return data

    











    

    # @validerrdecor
    # def to_read_model(self) -> BaseModel:
    #     '''Валидируем модель без поля id'''
    #     return self.pydantic_schema.model_validate(self.__dict__, from_attributes=True).model_dump()
    

    # @validerrdecor
    # def to_read_model_id(self) -> BaseModel:
    #     '''Валидируем модель с полем id'''
    #     # return self.pydantic_schema_id.model_validate(self.__dict__, from_attributes=True).model_dump()
    #     return self.pydantic_schema_id.model_validate(
    #         self.__dict__, from_attributes=True).model_dump()



    # @validerrdecor
    # # @staticmethod
    # def convert_ORM_model_in_dict(model, find_field=None, exlude_field=False) -> Base_Model:
    #     '''Подключаемся к данным колонок model'''  
    #     columns: list[Column] = model.__table__.columns
    #     '''Функция типизации данных колонки'''    
    #     type_value = lambda column=Column, default=...: Annotated[column.type.python_type | None, Field(default)]
    #     '''Выбираем все поля'''
    #     if not find_field:
    #         dict_types_columns = {column.name: type_value(column) for column in columns}
    #     '''Выибираем все поля кроме указанного'''
    #     if find_field and exlude_field == True:
    #         dict_types_columns = {column.name: type_value(column, None) for column in columns if not getattr(column, find_field)}
    #     '''Выибираем только указанное поле'''
    #     if find_field and exlude_field == False:
    #         dict_types_columns = {column.name: type_value(column) for column in columns if getattr(column, find_field)}
    #     return dict_types_columns

    
    # # @validerrdecor
    # def pydantic_dynamic_model(self, text=None, find_field=None, exlude_field=False, relation=False, dict_columns=None) -> Base_Model:
    #     '''Динамическое создание модели Pydantic на лету'''
    #     # правильное задание словаря или списка по умолчанию, в агрументах функции присваиваем значение None
    #     if dict_columns is None: dict_columns = {}
    #     '''Собираем словарь с элементами из колонок и их типов'''
    #     dict_columns = self.convert_ORM_model_in_dict(self, find_field, exlude_field)
    #     '''Одно из условий на нахождение всех связей из входного аргумента текуцей функции'''
    #     if relation:
    #         '''Проверяем все связи через метод inspect модели'''
    #         inspect_manager: Mapper = inspect(self)
    #         relationships: list[_RelationshipDeclared] = inspect_manager.relationships
    #         '''Пробегаем по всем связям'''
    #         for rel in relationships:
    #             '''Выбираем связи кроме lazy != select в асинхронном режиме она не грузится'''
    #             if rel.lazy != "select":
    #                 '''Узнаем класс модель из связи'''
    #                 class_rel: Base = rel.entity.class_
    #                 '''Рекурсия на начало функции для сбоора словаря из колонок текущей модели'''
    #                 text = "relationships"
    #                 rel_pydantic = self.pydantic_dynamic_model(class_rel, text=text, relation=True, dict_columns=dict_columns)
    #                 '''Создаем аннотацию типа из созданной схемы Pydantic'''
    #                 if rel.uselist:
    #                     rel_field = Annotated[list[rel_pydantic] | None, Field(...)]
    #                 else:
    #                     rel_field = Annotated[rel_pydantic | None, Field(...)]
    #                 '''Добавляем в родителя поле связи со полученной аннотацией'''
    #                 dict_columns[rel.key] = rel_field

    #     '''Подготавливаем имя будущего класса pydantic'''
    #     name_new_cls = f'Dynamic_model_{self.__tablename__}_{text}'
    #     '''Cоздание модели Pydantic'''
    #     return create_model(name_new_cls, **dict_columns)








    # repr_cols_num = 33
    # repr_cols = tuple()
    
    # def __repr__(self):
    #     """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
    #     cols = []
    #     for idx, col in enumerate(self.__table__.columns.keys()):
    #         if col in self.repr_cols or idx < self.repr_cols_num:
    #             cols.append(f"{col} = {getattr(self, col)}")

        # return f"<{self.__class__.__name__} {', '.join(cols)}>"
    
    # def __repr__(self):
    #     return f"<{self.__class__.__name__}>"

    # def __repr__(self):
    #     return f"{self.name}"


    
    # def pydantic_dynamic_model(self, find_field=None, exlude_field=False, relation=False) -> Base_Model:
    #     '''Динамическое создание модели Pydantic на лету'''
    #     '''Подключаемся к данным колонок model'''    
    #     columns: list[Column] = self.__table__.columns
    #     '''Функция типизации данных колонки'''    
    #     type_value = lambda column=Column, default=...: Annotated[column.type.python_type | None, Field(default)]
    #     '''Выбираем все поля'''
    #     if not find_field:
    #         dict_types_columns = {column.name: type_value(column) for column in columns}
    #     '''Выибираем все поля кроме указанного'''
    #     if find_field and exlude_field == True:
    #         dict_types_columns = {column.name: type_value(column, None) for column in columns if not getattr(column, find_field)}
    #     '''Выибираем только указанное поле'''
    #     if find_field and exlude_field == False:
    #         dict_types_columns = {column.name: type_value(column) for column in columns if getattr(column, find_field)}
    #     '''Выбираем вместе со связями, если они прописаны в модели как lazy='joined' '''
    #     if relation:
    #         inspect_manager: Mapper = inspect(self)
    #         relationships: list[_RelationshipDeclared] = inspect_manager.relationships
    #         for rel in relationships:
    #             if rel.lazy != "select":
    #                 # Класс связи
    #                 class_rel: Base = rel.entity.class_
    #                 # Колонки
    #                 rel_columns: list[Column] = class_rel.__table__.columns
    #                 # Словарь с типами колонок
    #                 rel_dict_types_columns = {column.name: type_value(column) for column in rel_columns}
    #                 # pydantic класс связей
    #                 rel_pydantic = create_model(f'DM_{self.__tablename__}_{rel.key}', **rel_dict_types_columns)
    #                 # Аннотация поля для родителя
    #                 if rel.uselist:
    #                     rel_field = Annotated[list[rel_pydantic] | None, Field(...)]
    #                 else:
    #                     rel_field = Annotated[rel_pydantic | None, Field(...)]
    #                 # Добавляем в родителя поле связи со полученной аннотацией
    #                 dict_types_columns[rel.key] = rel_field
    #     '''Cоздание модель Pydantic родителя'''
    #     return create_model(f'Dynamic_model_{self.__tablename__}', **dict_types_columns)