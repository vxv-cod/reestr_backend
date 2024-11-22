__all__ = ["Info"]

from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import intpk
# from apps.schemas.general import Schema_General, Schema_General_ID, Schema_General_ID_relations
from apps.schemas.general import Schema_General, Schema_General_ID_relations

# reestr_is
class Info(Base):
    '''ОБЩАЯ ИНФОРМАЦИЯ'''
    __tablename__ = "info"
    __table_args__ = {"comment": "ОБЩАЯ ИНФОРМАЦИЯ"}
    # schema = None
    # name = None
    
    # type_relationship = relationship(back_populates=__tablename__, lazy='joined')

    pydantic_schema = Schema_General
    pydantic_schema_id = Schema_General_ID_relations
    # model_json_schema: Schema_General_ID_relations
    

    id: Mapped[intpk]
    # Признак ИС/ИР
    sign_id: Mapped[int | None] = mapped_column(ForeignKey("sign.id", ondelete="CASCADE"), comment="Признак ИС/ИР")
    sign: Mapped["Sign"] = relationship(back_populates=__tablename__)

    # Наименование ИС/ИР (краткое)
    short_name: Mapped[str| None] = mapped_column(comment="Наименование ИС/ИР (краткое)")
    # Наименование ИС/ИР (полное)
    full_name: Mapped[str | None] = mapped_column(comment="Наименование ИС/ИР (полное)")
        
    # Каталог документов
    catalog: Mapped[str | None] = mapped_column(comment="Каталог документов")
    # directory_id: Mapped["Directory"] = relationship(back_populates=__tablename__, lazy='joined')

    
    # # Владелец ИС/ИР
    # owner_id: Mapped[str | None] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), comment="Владелец ИС/ИР")
    # # Бизнес-эксперт
    # business_expert_id: Mapped[str | None] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), comment="Бизнес-эксперт")
    # # Ответственный за сервисный компонент
    # responsible_service_component_id: Mapped[str | None] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), comment="Ответственный за сервисный компонент")
    # # Ответственный за ПЭД
    # responsible_PAD_id: Mapped[str | None] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), comment="Ответственный за ПЭД")
    # # Ответственный за согласование заявки на доступ
    # responsible_access_id: Mapped[str | None] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), comment="Ответственный за согласование заявки на доступ")
    

    # Этап эксплуатации
    stage_id: Mapped[int | None] = mapped_column(ForeignKey("stage.id", ondelete="CASCADE"), comment="Этап эксплуатации", nullable=True, default=None)
    stage: Mapped["Stage"] = relationship(back_populates = __tablename__)

    # Вид эксплуатации
    view_operation_id: Mapped[int | None] = mapped_column(ForeignKey("view_operation.id", ondelete="CASCADE"), comment="Вид эксплуатации")
    view_operation: Mapped["View_operation"] = relationship(back_populates = __tablename__)

    # Назначение ИС/ИР
    appointment: Mapped[str | None] = mapped_column(comment="Назначение ИС/ИР")

    '''# Уроверь конфиденциальности'''
    level_privacy_id: Mapped[int | None] = mapped_column(ForeignKey("level_privacy.id", ondelete="CASCADE"), comment=f"Уроверь конфиденциальности")
    level_privacy: Mapped["Level_privacy"] = relationship(back_populates = __tablename__)

    # Наличие обработки персональных данных
    processing_personal_data: Mapped[bool] = mapped_column(comment="Наличие обработки персональных данных", default=False)
    # Наличие обработки сведений конфиденциального характера 
    processing_confidential_information: Mapped[bool] = mapped_column(comment="Наличие обработки сведений конфиденциального характера", default=False)
    

    '''СЕРВИСНОЕ ОБСЛУЖИВАНИЕ'''
    # Доступность
    availability_id: Mapped[int | None] = mapped_column(ForeignKey("availability.id", ondelete="CASCADE"), comment="Доступность")
    availability: Mapped["Availability"] = relationship(back_populates = __tablename__)

    # Количество пользователей
    count_users: Mapped[int | None] = mapped_column(comment="Количество пользователей")
    
    # Структурные подразделения, использующие ИТ-сервис
    structural_divisions_id: Mapped[int | None] = mapped_column(ForeignKey("structural_divisions.id", ondelete="CASCADE"), comment="Структурные подразделения, использующие ИТ-сервис")
    structural_divisions: Mapped["Structural_divisions"] = relationship(back_populates = __tablename__)
    
    # Наличие удаленного доступа пользователей
    remote_access: Mapped[bool | None] = mapped_column(comment="Наличие удаленного доступа пользователей", default=False)
    # Наличие резервного копирования
    reserve: Mapped[bool | None] = mapped_column(comment="Наличие резервного копирования", default=False)
    
    # Сетевая конфигурация
    network_configuration_id: Mapped[int | None] = mapped_column(ForeignKey("network_configuration.id", ondelete="CASCADE"), comment="Сетевая конфигурация")
    network_configuration: Mapped["Network_configuration"] = relationship(back_populates = __tablename__)

    # Договор на обслуживание
    service_contract: Mapped[str | None] = mapped_column(comment="Договор на обслуживание")
    # Версия платформы
    platform_version_id: Mapped[int | None] = mapped_column(ForeignKey("platform_version.id", ondelete="CASCADE"), comment="Версия платформы")
    platform_version: Mapped["Platform_version"] = relationship(back_populates = __tablename__)

    # Использование УФИТ (10.28.66.234)
    using_UFIT: Mapped[bool | None] = mapped_column(comment="Использование УФИТ (10.28.66.234)", default=False)

    # Тип СУБД
    type_subd_id: Mapped[int | None] = mapped_column(ForeignKey("type_subd.id", ondelete="CASCADE"), comment="Тип СУБД")
    type_subd: Mapped["Type_subd"] = relationship(back_populates = __tablename__)

    # Версия СУБД
    version_subd: Mapped[str | None] = mapped_column(comment="Версия СУБД")
    
    '''# Размер выделенной памяти(текущий и планируемый в следующем году)'''
    # Eдиница измерения
    memory_size_unit_measure_id: Mapped[int | None] = mapped_column(ForeignKey("unit_measure.id", ondelete="CASCADE"), comment="Eдиница измерения")
    unit_measure: Mapped["Unit_measure"] = relationship(back_populates = __tablename__)
    # текущий
    memory_size_current: Mapped[int | None] = mapped_column(comment="текущий")
    # план
    memory_size_plan: Mapped[int | None] = mapped_column(comment="план")
    

    # Степень критичности
    degree_criticality_id: Mapped[int | None] = mapped_column(ForeignKey("degree_criticality.id", ondelete="CASCADE"), comment="Степень критичности")
    degree_criticality: Mapped["Degree_criticality"] = relationship(back_populates = __tablename__, lazy='joined')

    # Количество ОГ, используемых ИС
    count_DO: Mapped[int | None] = mapped_column(comment="Количество ОГ, используемых ИС")
    # Санкционнозависимость
    sanctions_dependence: Mapped[bool | None] = mapped_column(comment="Санкционнозависимость", default=False)




    # Ответственные лица
    # phonebook: Mapped[list["Phonebook"]] = relationship(
    #     back_populates = __tablename__,
    #     secondary = "responsible",
    #     # lazy='joined'
    # )
    signers_type: Mapped[list["Signers_type"]] = relationship(
        back_populates = __tablename__,
        secondary = "responsible",
        # lazy='joined'
    )

    # # Ответственные лица
    # responsible: Mapped[list["Responsible"]] = relationship(
    #     back_populates = __tablename__,
    #     # lazy='joined'
    # )

    # Аппаратное обеспечение с количеством, связь m2m
    hardware: Mapped[list["Hardware"]] = relationship(
        back_populates = __tablename__,
        secondary = "service_hardware",
        # lazy='joined'
    )

    # Программное обеспечение
    software: Mapped[list["Software"]] = relationship(
        back_populates = __tablename__,
        secondary = "service_software",
        # lazy='joined'
    )


    # Имена ВМ
    names_BM: Mapped[list["Names_BM"]] = relationship(
        back_populates = __tablename__,
        secondary = "service_names_BM",
        # lazy='joined'
    )

    '''ПЭД'''
    business_process: Mapped[list["Business_process"]] = relationship(
        back_populates=__tablename__,
        secondary = "ped_business_process",
        # lazy='joined'
        # lazy="subquery"
    )
    
    '''#   можно добавить lazy='joined' - m2o (o2o) или lazy='selectin' - o2m (m2o)'''
    doc_file: Mapped[list["Doc_file"]] = relationship(back_populates=__tablename__, 
        # lazy='joined'
    )












    # '''Многие к одному'''
    # '''Аннотационный способ записи'''
    # level_access_info: Mapped["Level_access_info"] = relationship(back_populates="general")
    # service_support: Mapped["Service_support"] = relationship(back_populates="general")
    # ped: Mapped["Ped"] = relationship(back_populates="general")

    # # '''Классический без аннотационный способ записи'''
    # level_access_info = relationship("Level_access_info", back_populates="generals")
    # service_support = relationship("Service_support", back_populates="generals")
    # ped = relationship("Ped", back_populates="generals")



# import inspect
# import sys
# classes = [getattr(sys.modules[__name__], name) for name in dir(sys.modules[__name__])
#            if inspect.isclass(getattr(sys.modules[__name__], name)) and getattr(sys.modules[__name__], name).__module__ == __name__]
# print(classes)
