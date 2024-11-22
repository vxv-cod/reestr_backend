__all__ = ["Directoryes"]

from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import name, intpk
from apps.schemas._name import SchemaName, SchemaName_ID


class Directory(Base):
    __tablename__ = "directory"
    __table_args__ = {"comment": "Каталог документов"}


    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    # id: Mapped[intpk]
    info_id: Mapped[int] = mapped_column(
        ForeignKey("info.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Информация"
    )
    name: Mapped[name]



    '''Связи'''
    info: Mapped["Info"] = relationship(back_populates=__tablename__)
    # doc_file: Mapped[Optional[list["Doc_file"]]] = relationship(back_populates=__tablename__, lazy="joined")
