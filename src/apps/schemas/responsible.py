from apps.schemas.__basemodel import Base_Model


class Schema_responsible(Base_Model):
    # id: int = None
    info_id: int
    phonebook_id: str
    signers_type_id: int

