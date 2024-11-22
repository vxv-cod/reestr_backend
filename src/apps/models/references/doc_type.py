__all__ = ["Doc_type"]

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import name, intpk
from apps.schemas._name import SchemaName, SchemaName_ID


class Doc_type(Base):
    __tablename__ = "doc_type"
    __table_args__ = {"comment": "Тип документации"}


    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]

    '''Связи'''
    doc_file: Mapped[Optional[list["Doc_file"]]] = relationship(back_populates=__tablename__)
