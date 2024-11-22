__all__ = ["Sign"]

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import intpk, name
from apps.schemas._name import SchemaName, SchemaName_ID



class Sign(Base):
    __tablename__ = "sign"
    __table_args__ = {"comment": "Признак ИС/ИР"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]
    
    # '''Свзяь один ко многим'''
    info: Mapped[list["Info"]] = relationship(back_populates=__tablename__)