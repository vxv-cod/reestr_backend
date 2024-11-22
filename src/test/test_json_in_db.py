import asyncio
import sys, os
import types
from loguru import logger
from sqlalchemy import Inspector, delete, inspect
from rich import print


if __name__ == "__main__":
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    

from apps.db import Base
from apps.db import async_engine, sync_engine, sync_session_maker
from apps.models._base.info import Info
from apps.models.references.availability import Availability
from apps.repositories.repo_SQL import SQLRepo
from apps.repositories.repo_uow import UnitOfWork



async def sqlgo(table, data, uow: UnitOfWork):
    uow_attr: SQLRepo = getattr(uow, table)
    await uow.session.execute(delete(uow_attr.model))
    await uow.session.flush()
    await uow_attr.add_list(data)
    await uow.session.flush()  



async def sqlmultisave(obj: dict, uow: UnitOfWork):
    for key, val in obj.items():
        if isinstance(val, list):
            await sqlgo(key, val, uow)
            for item in val:
                if isinstance(item, dict):
                    await sqlmultisave(item, uow)
                    


# async def sqlmultisave(table: dict, uow: UnitOfWork):
#     await sqlgo("service_support", table, uow)
#     for i in table.values():
#         if isinstance(i, dict) and i["data"] != []:
#             await sqlgo(i["tablename"], i["data"], uow)



async def add_general_info(uow: UnitOfWork = UnitOfWork()):
    data_json = {
        "info": [
            {
                "id": 0,
                "sign_id": 0,
                "short_name": "ИС «СРК»",
                "full_name": "Система резервного копирования ООО «ТННЦ»",
                "stage_id": 4,
                "view_operation_id": 0,
                "appointment": "Система резервного копирования данных ООО «ТННЦ»",
                "owner_id": "991b1152-ddc5-4352-b66f-64faa4bd8c88",
                "business_expert_id": "2fc34204-0099-4943-b13a-0b8c68f25932",
                "responsible_service_component_id": "2dbe12bb-b8d2-4716-bb91-28430dc436f9",
                "responsible_PAD_id": "19afdee2-ab5e-4450-adbf-f3f5466decf4",
                "responsible_access_id": None
            },
            {
                "id": 1,
                "sign_id": 0,
                "short_name": "ИС «СЭД Directum» / ИС «СЭД Directum ЮЗДО»",
                "full_name": "Система электронного документооборота DIRECTUM / Система электронного документооборота DIRECTUM юридически значимый документооборот",
                "stage_id": 4,
                "view_operation_id": 2,
                "appointment": "Система электронного документооборота, контроль исполнения поручений по документам ",
                "owner_id": "626fcb94-39f8-4000-9e73-3484305d57f4",
                "business_expert_id": "626fcb94-39f8-4000-9e73-3484305d57f4",
                "responsible_service_component_id": "598504e1-7e90-4192-8e89-c26db9a48f14",
                "responsible_PAD_id": "598504e1-7e90-4192-8e89-c26db9a48f14",
                "responsible_access_id": "626fcb94-39f8-4000-9e73-3484305d57f4"
            }
        ],

        "service_support": [
            {
                "id": 0,
                "availability_id": 0,
                "count_users": None,
                "structural_divisions_id": 16,
                "remote_access": 0,
                "reserve": 0,
                "network_configuration_id": 2,
                "service_contract": None,
                "platform_version_id": None,
                "using_UFIT": 0,
                "type_subd_id": 3,
                "version_subd": None,
                "memory_size_unit_measure_id": None,
                "memory_size_current": None,
                "memory_size_plan": None,
                "degree_criticality_id": None,
                "count_DO": None,
                "sanctions_dependence": None,
                "service_hardware": [
                    {
                        "service_support_id": 0,
                        "hardware_id": 14,
                        "hardware_count": 2
                    },
                    {
                        "service_support_id": 0,
                        "hardware_id": 15,
                        "hardware_count": 2
                    },
                    {
                        "service_support_id": 0,
                        "hardware_id": 23,
                        "hardware_count": 3
                    }
                ],
                "service_software": [
                    {
                        "service_support_id": 0,
                        "software_id": 59
                    },
                    {
                        "service_support_id": 0,
                        "software_id": 52
                    },
                    {
                        "service_support_id": 0,
                        "software_id": 116
                    }
                ],
                "service_names_BM": [
                    {
                        "service_support_id": 0,
                        "names_BM_id": 0
                    },
                    {
                        "service_support_id": 0,
                        "names_BM_id": 1
                    },
                    {
                        "service_support_id": 0,
                        "names_BM_id": 2
                    }
                ],
            },
            {
                "id": 1,
                "availability_id": 0,
                "count_users": None,
                "structural_divisions_id": 16,
                "remote_access": 0,
                "reserve": 0,
                "network_configuration_id": 2,
                "service_contract": None,
                "platform_version_id": None,
                "using_UFIT": 0,
                "type_subd_id": 3,
                "version_subd": None,
                "memory_size_unit_measure_id": None,
                "memory_size_current": None,
                "memory_size_plan": None,
                "degree_criticality_id": None,
                "count_DO": None,
                "sanctions_dependence": None,
                "service_hardware": [
                    {
                        "service_support_id": 1,
                        "hardware_id": 10,
                        "hardware_count": 3
                    },
                    {
                        "service_support_id": 1,
                        "hardware_id": 9,
                        "hardware_count": 2
                    },
                    {
                        "service_support_id": 1,
                        "hardware_id": 8,
                        "hardware_count": 3
                    }
                ],
                "service_software": [
                    {
                        "service_support_id": 1,
                        "software_id": 44
                    },
                    {
                        "service_support_id": 1,
                        "software_id": 55
                    },
                    {
                        "service_support_id": 1,
                        "software_id": 66
                    }
                ],
                "service_names_BM": [
                    {
                        "service_support_id": 1,
                        "names_BM_id": 3
                    },
                    {
                        "service_support_id": 1,
                        "names_BM_id": 4
                    },
                    {
                        "service_support_id": 1,
                        "names_BM_id": 5
                    }
                ],
            },

        ],

        "level_access_info": [
            {
                "id": 0,
                "level_privacy_id": 0,
                "processing_personal_data": 0,
                "processing_confidential_information": 0
            },
            {
                "id": 1,
                "level_privacy_id": 1,
                "processing_personal_data": 1,
                "processing_confidential_information": 1
            },

        ],
    }

    async with uow:
        await sqlmultisave(data_json, uow)
        await uow.commit()    



if __name__ == "__main__":
    asyncio.run(add_general_info())
    



    

























