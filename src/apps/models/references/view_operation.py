__all__ = ["View_operation"]

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import strpk, intpk, name
from apps.schemas._name import SchemaName, SchemaName_ID



class View_operation(Base):
    __tablename__ = "view_operation"
    __table_args__ = {"comment": "Вид эксплуатации"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]
    
    # '''Свзяь один ко многим'''
    info: Mapped[list["Info"]] = relationship(back_populates=__tablename__)    