from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    department_name: str = Field(..., min_length=1, max_length=200)


class DepartmentCreate(DepartmentBase):
    parent_department_id: Optional[str] = None
    manager_id: str


class DepartmentUpdate(DepartmentBase):
    parent_department_id: Optional[str] = None
    manager_id: str


class DepartmentInDBBase(DepartmentBase):
    id: str
    manager_id: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    proxy_manager_id: Optional[int] = None
    parent_department_id: Optional[str] = None
    sub_departments: List[str] = Field(default_factory=list)
    roles: Optional[List[str]] = Field(default_factory=list)
    permissions: Optional[List[str]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class Department(DepartmentInDBBase):
    pass


class DepartmentInDB(DepartmentInDBBase):
    pass
