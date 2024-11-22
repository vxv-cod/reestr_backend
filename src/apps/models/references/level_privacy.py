__all__ = ["Level_privacy"]

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import strpk, intpk, name
from apps.schemas._name import SchemaName, SchemaName_ID



class Level_privacy(Base):
    __tablename__ = "level_privacy"
    __table_args__ = {"comment": "Уровень конфиденциальности"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID
    
    id: Mapped[intpk]
    name: Mapped[name]

    # '''Свзяь один ко многим'''
    info: Mapped[list["Info"]] = relationship(back_populates=__tablename__)    