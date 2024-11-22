from typing import Annotated, Union
from fastapi import Depends
from pydantic import Field, create_model
from sqlalchemy import inspect
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.orm.relationships import _RelationshipDeclared
# from rich import print
from loguru import logger

from apps.db import Base
from apps.schemas.__basemodel import Base_Model



class AutoSchema:
    '''Автогенерация pydantic сххем'''
    def __init__(self, orm_model: Base) -> None:
        self.model = orm_model
        self.inspect_manager: Mapper = inspect(self.model)
        self.ALL = self.pydantic_dynamic_model(model=self.model, text="ALL")
        self.ALL_i_REL = self.pydantic_dynamic_model(model=self.model, text="ALL_i_REL", relation=True)
        self.IN = self.compute_db_schema_in()
        self.PK_only = Annotated[
            self.pydantic_dynamic_model(
                model=self.model, text="PK_only", only_primary_key=True
            ), 
            Depends()
        ]


    def compute_db_schema_in(self):
        '''При наличии primary_key больше одного в таблице принимаем схему всех полей, 
        иначе схему без поля primary_key'''
        if len(self.model.__table__.primary_key) > 1:
            return self.ALL
        else:
            return self.pydantic_dynamic_model(model=self.model, text="PK_not", not_primary_key=True)


    def include_in_schema(self):
        '''Проверяем загружены ли связи при запросе'''
        relationships: list[_RelationshipDeclared] = self.inspect_manager.relationships
        count_relationships = sum([1 for rel in relationships if rel.lazy != "select"])
        if count_relationships == 0: 
            return False
        else: 
            return True

    @staticmethod
    def convert_ORM_model_in_dict(model: Base, not_primary_key: bool = False, only_primary_key: bool = False) -> Union[dict, list[dict]]:
        '''Подключаемся к данным колонок model'''
        columns: list[Column] = model.__table__.columns
        '''Функция типизации данных колонки'''    
        type_value = lambda column=Column, default=...: Annotated[column.type.python_type | None, Field(default)]
        '''Выибираем только primary_key'''
        if only_primary_key == True:
            return {column.name: type_value(column) for column in columns if getattr(column, "primary_key")}
        '''Выбираем все поля'''
        if not_primary_key == False:
            return {column.name: type_value(column) for column in columns}
        '''Выибираем все поля кроме primary_key'''
        if not_primary_key == True:
            return {column.name: type_value(column, None) for column in columns if not getattr(column, "primary_key")}
        

    def pydantic_dynamic_model(self, model: Base, text=None, relation=False, not_primary_key=False, only_primary_key=False, dict_columns=None) -> Base_Model:
        '''Динамическое создание модели Pydantic на лету'''
        # правильное задание словаря или списка по умолчанию, в агрументах функции присваиваем значение None
        if dict_columns is None: 
            dict_columns = {}

        '''Собираем словарь с элементами из колонок и их типов'''
        dict_columns = self.convert_ORM_model_in_dict(model, not_primary_key, only_primary_key)
        '''Одно из условий на нахождение всех связей из входного аргумента текуцей функции'''
        if relation:
            '''Проверяем все связи через метод inspect модели'''
            inspect_manager: Mapper = inspect(model)
            relationships: list[_RelationshipDeclared] = inspect_manager.relationships
            '''Пробегаем по всем связям'''
            for rel in relationships:
                '''Выбираем связи кроме lazy != select в асинхронном режиме она не грузится'''
                if rel.lazy != "select":
                    '''Узнаем класс модель из связи'''
                    class_rel = rel.entity.class_
                    '''Рекурсия на начало функции для сбоора словаря из колонок текущей модели'''
                    text = "relationships"
                    rel_pydantic = self.pydantic_dynamic_model(class_rel, text, True, not_primary_key, only_primary_key, dict_columns)
                    '''Создаем аннотацию типа из созданной схемы Pydantic'''
                    rel_field = Annotated[Union[list[rel_pydantic], rel_pydantic, None], Field(...)]
                    '''Добавляем в родителя поле связи со полученной аннотацией'''
                    dict_columns[rel.key] = rel_field
        '''Подготавливаем имя будущего класса pydantic'''
        name_new_cls = f'Dynamic_model_{model.__tablename__}_{text}'
        '''Cоздание модели Pydantic'''
        return create_model(name_new_cls, **dict_columns)









    # def convert_ORM_model_in_dict(self, model, find_field, exlude_field) -> dict | list[dict]:
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
    #     # if find_field and exlude_field == False:
    #     #     dict_types_columns = {column.name: type_value(column) for column in columns if getattr(column, find_field)}
    #     if find_field and exlude_field == False:
    #         dict_types_columns = {column.name: type_value(column) for column in columns if getattr(column, "primary_key")}
    #     return dict_types_columns


    # def pydantic_dynamic_model(self, model, text=None, find_field=None, exlude_field=False, relation=False, dict_columns=None) -> Base_Model:
    #     '''Динамическое создание модели Pydantic на лету'''
    #     # правильное задание словаря или списка по умолчанию, в агрументах функции присваиваем значение None
    #     if dict_columns is None: dict_columns = {}
    #     '''Собираем словарь с элементами из колонок и их типов'''
    #     dict_columns = self.convert_ORM_model_in_dict(model, find_field, exlude_field)
    #     '''Одно из условий на нахождение всех связей из входного аргумента текуцей функции'''
    #     if relation:
    #         '''Проверяем все связи через метод inspect модели'''
    #         inspect_manager: Mapper = inspect(model)
    #         relationships: list[_RelationshipDeclared] = inspect_manager.relationships
    #         '''Пробегаем по всем связям'''
    #         for rel in relationships:
    #             '''Выбираем связи кроме lazy != select в асинхронном режиме она не грузится'''
    #             if rel.lazy != "select":
    #                 '''Узнаем класс модель из связи'''
    #                 class_rel = rel.entity.class_
    #                 '''Рекурсия на начало функции для сбоора словаря из колонок текущей модели'''
    #                 text = "relationships"
    #                 rel_pydantic = self.pydantic_dynamic_model(model=class_rel, text=text, relation=True, dict_columns=dict_columns)
    #                 '''Создаем аннотацию типа из созданной схемы Pydantic'''
    #                 if rel.uselist:
    #                     rel_field = Annotated[list[rel_pydantic] | None, Field(...)]
    #                 else:
    #                     rel_field = Annotated[rel_pydantic | None, Field(...)]
    #                 '''Добавляем в родителя поле связи со полученной аннотацией'''
    #                 dict_columns[rel.key] = rel_field
    #     '''Подготавливаем имя будущего класса pydantic'''
    #     name_new_cls = f'Dynamic_model_{model.__tablename__}_{text}'
    #     '''Cоздание модели Pydantic'''
    #     return create_model(name_new_cls, **dict_columns)


