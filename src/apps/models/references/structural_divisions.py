__all__ = ["Structural_divisions"]

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import name, intpk
from apps.schemas._name import SchemaName, SchemaName_ID



class Structural_divisions(Base):
    __tablename__ = "structural_divisions"
    __table_args__ = {"comment": "Структурные подразделения, использующие ИТ-сервис"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]
    
    # '''Свзяь один ко многим'''
    info: Mapped[list["Info"]] = relationship(back_populates=__tablename__)