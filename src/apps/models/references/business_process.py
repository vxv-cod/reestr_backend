__all__ = ["Business_process"]

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import intpk, strpk, name
from apps.schemas._name import SchemaNameStr, SchemaNameStr_ID



class Business_process(Base):
    __tablename__ = "business_process"
    __table_args__ = {"comment": "Бизнес-процесс"}

    pydantic_schema = SchemaNameStr
    pydantic_schema_id = SchemaNameStr_ID

    id: Mapped[strpk]
    # id: Mapped[str] = mapped_column(primary_key=True, comment="Шифр")
    name: Mapped[name]

    
    info: Mapped[list["Info"] | None] = relationship(
        back_populates = __tablename__,
        secondary="ped_business_process",
    )