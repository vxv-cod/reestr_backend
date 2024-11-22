from apps.schemas.__basemodel import Base_Model


class Schema_file_status_file(Base_Model):
    file_status_id: int
    file_data_id: int


class Schema_file_status_file_ID(Schema_file_status_file):
    id: int

