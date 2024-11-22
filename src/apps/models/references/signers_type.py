__all__ = ["Signers_type"]

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import intpk, name
from apps.schemas._name import SchemaName, SchemaName_ID



class Signers_type(Base):
    __tablename__ = "signers_type"
    __table_args__ = {"comment": "Роль ответственного"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]
    
    # responsible: Mapped[list["Responsible"]] = relationship(back_populates = __tablename__)


    info: Mapped[list["Info"]] = relationship(
        back_populates = __tablename__,
        secondary = "responsible",
    )