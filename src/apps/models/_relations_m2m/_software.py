__all__ = ["Software"]

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import strpk, intpk, name
from apps.schemas._name import SchemaName, SchemaName_ID




class Software(Base):
    __tablename__ = "software"
    __table_args__ = {"comment": "Программное обеспечение"}

    pydantic_schema = SchemaName
    pydantic_schema_id = SchemaName_ID

    id: Mapped[intpk]
    name: Mapped[name]
    
    info: Mapped[list["Info"]] = relationship(
        back_populates = __tablename__,
        secondary="service_software",
    )