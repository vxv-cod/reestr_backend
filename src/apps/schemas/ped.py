import datetime
from typing import Any
from apps.schemas.__basemodel import Base_Model
from apps.schemas.file_data import Schema_file_data_ID, Schema_file_data_ID_relation
from apps.schemas.ped_biseness import Schema_ped_business_process
from apps.schemas._name import SchemaNameStr, SchemaNameStr_ID



class SchemaPed(Base_Model):
    id: int


class SchemaPed_relationship(SchemaPed):
    business_process: list[SchemaNameStr_ID]
    doc_file: list[Schema_file_data_ID_relation]

    # general: "Info"





    # # Приказ (дата, №)
    # prikaz_id: int | None

    # '''Проектная и управленческая документация'''
    # # ВТР
    # vtr: int | None
    # # ФТТ/ТЗ
    # ftt_tz: int | None
    # # Перечень информации, используемой в бизнес-процессе
    # pereahen_info: int | None
    # # Решение о категорировании информации (РОК)
    # rok: int | None
    # # Технический проект (ТПр)
    # tpr: int | None
    # # Программа и методика испытаний (ПиМИ)
    # pimi: int | None
    # # Программа и методика испытаний на соответствие требованиям ИБ
    # prog_ib: int | None
    # # Результаты проведенных испытаний (Протокол ПСИ)
    # protocol_psi: int | None
    # # Протокол ОС/УС о готовности к старту этапа эксплуатации
    # protocol_os_ys: int | None
    # # Протокол приема-передачи в сопровождение ИС/ИР 
    # protocol_is_ir: int | None
    # # Акт о готовности ИС/ИР к вводу в промышленную эксплуатацию
    # akt_gotov_is_ir: int | None

    # '''Эксплуатационная документация'''
    # # Технический паспорт (ТПс)
    # tps: int | None
    # # Регламент предоставления доступа (РПД)
    # rpd: int | None
    # # Руководство по обеспечению непрерывности
    # rukovodstvo_neprer: int | None
    # # Инструкция пользователя
    # manual_user: int | None
    # # Инструкция администратора
    # manual_admin: int | None