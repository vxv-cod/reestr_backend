from types import NoneType
from typing import Annotated, Any, Union
from pydantic import BeforeValidator, AfterValidator, PlainValidator, WrapValidator, ValidationInfo, ValidatorFunctionWrapHandler, computed_field, field_validator, model_validator
from apps.db import Base
from apps.models._relations_m2m._hardware import Hardware
from apps.models._relations_m2m._names_BM import Names_BM
from apps.models._relations_m2m._software import Software
from apps.schemas.__basemodel import Base_Model
from apps.schemas._name import SchemaNameStr, SchemaNameStr_ID
from apps.schemas.file_data import Schema_file_data_ID, Schema_file_data_ID_relation
from apps.schemas._name import SchemaName, SchemaName_ID
# from rich import print
from apps.schemas.__basemodel import Base_Model_id





class Schema_Info(Base_Model):
    # Признак ИС/ИР
    sign_id: int | None = None
    # Наименование ИС/ИР (краткое)
    short_name: str | None = None
    # Наименование ИС/ИР (полное)
    full_name: str | None = None
    # Этап эксплуатации
    stage_id: int | None = None
    # Вид эксплуатации
    view_operation_id: int | None = None
    # Назначение ИС/ИР
    appointment: str | None = None
    catalog: str | None = None


# type_list_id = MyName = Annotated[list[Union[Base_Model_id, int, str]], AfterValidator(lambda v: [i.id if not isinstance(i, int | str) else i for i in v])]


class Schema_Info_relations(Base_Model):
    # Аппаратное обеспечение 
    hardware: list[SchemaName_ID]
    # Программное обеспечение
    software: list[SchemaName_ID]
    # Имена ВМ
    names_BM: list[SchemaName_ID]
    # Бизнес-процесс
    business_process: list[SchemaNameStr_ID]
    # Документация
    doc_file: list[Schema_file_data_ID]


    # # Аппаратное обеспечение 
    # hardware: type_list_id
    # # Программное обеспечение
    # software: type_list_id
    # # Имена ВМ
    # names_BM: type_list_id
    # # Бизнес-процесс
    # business_process: type_list_id
    # # Документация
    # doc_file: type_list_id
    




    # @model_validator(mode='after')
    # def valid_after(self):
    #     print(f"after = {self.hardware}")
    #     self.hardware = [i.name if not isinstance(i, str) else i for i in self.hardware]
    #     return self   

    # @model_validator(mode='before')
    # @classmethod
    # def valid(cls, data: Any):
    #     print(f"before 111= {data['hardware']}")
    #     # data["hardware"] = [i.name if not isinstance(i, str) else i for i in data["hardware"]]

    #     return data   


# def func_WrapValidator(v, handler):
#     print("func_WrapValidator")
#     return [i.id if not isinstance(i, int | str) else i for i in v]

# # MyName = Annotated[list[SchemaName_ID | str], AfterValidator(lambda v: [i.id if not isinstance(i, str) else i for i in v])]
    
# MyName = Annotated[list[Union[Base_Model_id, int, str]], WrapValidator(lambda v, handler: [i.id if not isinstance(i, int | str) else i for i in v])]
# MyName = Annotated[list[Union[Base_Model_id, int, str]], WrapValidator(func_WrapValidator)]    
# type_list_id = MyName = Annotated[list[Union[Base_Model_id, int, str]], AfterValidator(lambda v: [i.id if not isinstance(i, int | str) else i for i in v])]
    

        # # Владелец ИС/ИР
    # owner_id: str | None
    # # Бизнес-эксперт
    # business_expert_id: str | None
    # # Ответственный за сервисный компонент
    # responsible_service_component_id: str | None
    # # Ответственный за ПЭД
    # responsible_PAD_id: str | None
    # # Ответственный за согласование заявки на доступ
    # responsible_access_id: str | None