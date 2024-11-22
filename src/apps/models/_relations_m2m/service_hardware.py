__all__ = ["Service_hardware"]

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from apps.db import Base
from apps.schemas.service_support import SchemaServiceHardware



class Service_hardware(Base):
    __tablename__ = "service_hardware"
    __table_args__ = {"comment": "Аппаратное обеспечение"}

    pydantic_schema = SchemaServiceHardware
    pydantic_schema_id = SchemaServiceHardware

    info_id: Mapped[int] = mapped_column(
        ForeignKey("info.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Id системы"
    )
    hardware_id: Mapped[int] = mapped_column(
        ForeignKey("hardware.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Наименование"
    )

    hardware_count: Mapped[int | None] = mapped_column(comment="Кол.-во")