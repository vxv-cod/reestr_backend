__all__ = ["Stage"]

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import name, intpk
from apps.schemas._name import SchemaName, SchemaName_ID



class Stage(Base):
    __tablename__ = "stage"
    __table_args__ = {"comment": "Этап эксплуатации"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]
    
    # '''Свзяь один ко многим'''
    info: Mapped[list["Info"]] = relationship(back_populates=__tablename__)    