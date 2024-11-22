__all__ = ["Doc_file"]

import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import strpk, intpk, name
from apps.schemas.file_data import Schema_file_data, Schema_file_data_ID



class Doc_file(Base):
    __tablename__ = "doc_file"
    __table_args__ = {"comment": "Файл"}
    
    pydantic_schema = Schema_file_data
    pydantic_schema_id = Schema_file_data_ID

    id: Mapped[intpk]
    name: Mapped[name]
    info_id: Mapped[int] = mapped_column(
        ForeignKey("info.id", ondelete="CASCADE"), 
        comment="Информация"
    )
    doc_type_id: Mapped[int] = mapped_column(
        ForeignKey("doc_type.id", ondelete="CASCADE"), 
        comment="Тип документации"
    )
    # patch: Mapped[str | None] = mapped_column(comment="Полный адрес файла")
    # date: Mapped[datetime.date | None] = mapped_column(comment="Дата")
    # nomer: Mapped[str | None] = mapped_column(comment="Номер")

    
    '''Связи'''
    doc_type: Mapped["Doc_type"] = relationship(back_populates=__tablename__, lazy='joined')
    info: Mapped["Info"] = relationship(back_populates=__tablename__)



    # prikaz: Mapped[Optional["Prikaz"]] = relationship(back_populates=__tablename__)
    # ped_id: Mapped[int] = mapped_column(
    #     ForeignKey("ped.id", ondelete="CASCADE"), 
    #     comment="ПЭД"
    # )    
    # ped: Mapped[Optional["Ped"]] = relationship(back_populates=__tablename__)

    # doc_resource: Mapped[Optional["Doc_resource"]] = relationship(back_populates=__tablename__)
    # doc_resource_id: Mapped[int] = mapped_column(
    #     ForeignKey("doc_resource.id", ondelete="CASCADE"), 
    #     comment="Ресурс"
    # )
    # catalog: Mapped[str | None] = mapped_column(comment="Полный адрес файла")
    # name: Mapped[name]

    # doc_status: Mapped[Optional["Doc_status"]] = relationship(back_populates=__tablename__)

    # doc_status_id: Mapped[int] = mapped_column(
    #     ForeignKey("doc_status.id", ondelete="CASCADE"), 
    #     comment="Cтатус документа"
    # )

    # list_izm: Mapped[list["List_izm"]] = relationship(back_populates=__tablename__)

    # Ссылка на ресурс с документами
    # file_resource_id: Mapped[str | None] = mapped_column(ForeignKey("file_resource.id", ondelete="CASCADE"), comment=f"Ссылка на ресурс с документами")
    