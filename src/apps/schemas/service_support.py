from typing import Annotated, Any, Union
from pydantic import Field, PlainValidator, model_validator
from apps.schemas.__basemodel import Base_Model
from apps.schemas._name import SchemaName, SchemaName_ID
from apps.schemas.service_names_BM import Schema_service_names_BM


class SchemaServiceSupport(Base_Model):
    '''СЕРВИСНОЕ ОБСЛУЖИВАНИЕ'''
    # Доступность
    availability_id: int | None = None
    # Количество пользователей
    count_users: int | None = None
    # Структурные подразделения, использующие ИТ-сервис
    structural_divisions_id: int | None = None
    # Наличие удаленного доступа пользователей
    remote_access: bool | None = False
    # Наличие резервного копирования
    reserve: bool | None = False
    # Сетевая конфигурация
    network_configuration_id: int | None = None

    # Договор на обслуживание
    service_contract: str | None = None
    # Версия платформы
    platform_version_id: int | None = None
    # Использование УФИТ (10.28.66.234)
    using_UFIT: bool | None = False

    # Тип СУБД
    type_subd_id: int | None = None
    # Версия СУБД
    version_subd: str | None = None
    # Размер выделенной памяти(текущий и планируемый в следующем году)
    # Eдиница измерения
    memory_size_unit_measure_id: int | None = None
    # текущий
    memory_size_current: int | None = None
    # план
    memory_size_plan: int | None = None

    # Степень критичности
    degree_criticality_id: int | None = None
    
    # Сколькими ДО РН используется (Количество ОГ, используемых ИС)
    count_DO: int | None = None

    # Санкционнозависимость
    sanctions_dependence: bool | None = False




# class SchemaWare(Base_Model):
#     name: str | None    
#     info: list["SchemaServiceSupport"]

# class SchemaWare_ID(SchemaWare):
#     id: int



class SchemaServiceHardware(Base_Model):
    info_id: int
    hardware_id: int
    hardware_count: int | None = None

class SchemaServiceSoftware(Base_Model):
    info_id: int
    software_id: int

# class SchemaServiceSupport_relations(Base_Model):
#     # # Аппаратное обеспечение 
#     hardware: list[SchemaName_ID | str]
#     # Программное обеспечение
#     software: list[SchemaName_ID | str]
#     # Имена ВМ
#     names_BM: list[SchemaName_ID | str]







    # hardware: Union[list[SchemaName_ID], str]
    # # Программное обеспечение
    # software: list["SchemaName_ID"] | str
    # # Имена ВМ
    # names_BM: list["SchemaName_ID"] | str
    # Аппаратное обеспечение 
    # hardware: Union[list, str]

    # @model_validator(mode='after')
    # def valid_Service(self):
    #     if self.hardware != []: self.hardware = [i.name for i in self.hardware]
    #     # if self.software != []: self.software = [i.name for i in self.software]
    #     # if self.names_BM != []: self.names_BM = [i.name for i in self.names_BM]
    #     return self        

# from apps.schemas.info import Schema_Info

# class SchemaServiceSupport_relationship(SchemaServiceSupport):
#     general: Schema_Info
    

    # MyTimestamp = Annotated[datetime, WrapValidator(validate_timestamp)]
