from apps.schemas.__basemodel import Base_Model


class SchemaChecklist(Base_Model):
    # НАИМЕНОВАНИЕ ДОКУМЕНТА В СОСТАВЕ КОМПЛЕКТА
    name: str | None
    # ПРИМЕНИМОСТЬ ДЛЯ ИС/ИР
    sign_id: int
    '''ОБЯЗАТЕЛЬНОСТЬ УТВЕРЖДЕНИЯ ДОКУМЕНТА ДЛЯ ПЕРЕХОДА НА ЭТАП ЭКСПЛУАТАЦИИ'''
    # ТЕСТОВАЯ
    test: bool
    # ОПЫТНАЯ
    experience: bool
    # ОПЫТНО-ПРОМЫШЛЕННАЯ
    pilot_industrial: bool
    # ПРОМЫШЛЕННАЯ
    industrial: bool
    
class SchemaChecklist_ID(SchemaChecklist):
    id: int
