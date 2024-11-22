__all__ = ["Unit_measure"]

from sqlalchemy.orm import Mapped, relationship

from apps.db import Base
from apps.dependencies.dep_models import strpk, intpk, name
from apps.schemas._name import SchemaName, SchemaName_ID



class Unit_measure(Base):
    __tablename__ = "unit_measure"
    __table_args__ = {"comment": "Eдиница измерения"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]

    # '''Свзяь один ко многим'''
    info: Mapped[list["Info"]] = relationship(back_populates=__tablename__)    