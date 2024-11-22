

from pydantic import model_validator
from apps.schemas.__basemodel import Base_Model


class SchemaPhonebook(Base_Model):
    id: str
    employeeFullName: str | None
    departmentName: str | None
    staffPosName: str | None
    phone: str | None
    phoneInternal: str | None
    phoneMobile: str | None
    numberCabinet: str | None
    username: str | None
    house: str | None
    
    @model_validator(mode='after')
    def valid(self):
        if self.phoneInternal and "86-020-" in self.phoneInternal:
            self.phoneInternal: str = self.phoneInternal.split("86-020-")[-1]
        return self
    
