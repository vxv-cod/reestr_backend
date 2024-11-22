__all__ = ["Type_subd"]

from sqlalchemy.orm import Mapped, relationship

from apps.db import Base
from apps.dependencies.dep_models import strpk, intpk, name
from apps.schemas._name import SchemaName, SchemaName_ID



class Type_subd(Base):
    __tablename__ = "type_subd"
    __table_args__ = {"comment": "Тип СУБД"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]

    # '''Свзяь один ко многим'''
    info: Mapped[list["Info"]] = relationship(back_populates=__tablename__)