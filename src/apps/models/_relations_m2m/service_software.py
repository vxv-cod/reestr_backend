__all__ = ["Service_software"]

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.schemas.service_support import SchemaServiceSoftware



class Service_software(Base):
    __tablename__ = "service_software"
    __table_args__ = {"comment": "Программное обеспечение"}

    pydantic_schema = SchemaServiceSoftware
    pydantic_schema_id = SchemaServiceSoftware

    info_id: Mapped[int] = mapped_column(
        ForeignKey("info.id", ondelete="CASCADE"),
        primary_key=True,
    )
    software_id: Mapped[int] = mapped_column(
        ForeignKey("software.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Наименование"
    )
