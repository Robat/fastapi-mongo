from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

from ..models.department import Department
from ..database.connection import get_db_client, AsyncIOMotorClient
from app.config.settings import get_settings
from app.config.auth import get_current_user

router = APIRouter()
settings = get_settings()


@router.get("/departments", response_model=List[Department])
async def get_departments(current_user: str = Depends(get_current_user), db: AsyncIOMotorClient = Depends(get_db_client)):
    table = db[settings.MONGODB_DATABASE_NAME]["departments"]
    cursor = table.find()

    departments = []
    async for document in cursor:
        # 根據您的資料庫結構，適當修改欄位名稱
        departments.append(Department(
            id=str(document["_id"]),
            department_name=document["department_name"],
            manager_id=str(document["manager_id"]),  # 將 manager_id 轉換為字符串
        ))

    return departments
