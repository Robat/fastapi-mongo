import pymongo
from bson.objectid import ObjectId
from datetime import datetime

# 建立連接
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hmconsulting"]

# 插入部門資料
departments = db["departments"]
department_data = {
    "department_name": "IT",
    "description": "Information Technology",
}
department_result = departments.insert_one(department_data)
department_id = department_result.inserted_id

# 插入員工資料
employees = db["employees"]
employee_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "position": "Software Engineer",
    "department_id": department_id,
}
employee_result = employees.insert_one(employee_data)
employee_id = employee_result.inserted_id

# 插入用戶資料
users = db["users"]
user_data = {
    "username": "johndoe",
    "password_hash": "hashed_password",
    "role": "employee",
    "permissions": ["view_reports"],
    "employee_id": employee_id,
}
user_result = users.insert_one(user_data)
user_id = user_result.inserted_id

# 插入管理員資料
managers = db["managers"]
manager_data = {
    "employee_id": employee_id,
    "user_id": user_id,
    "managed_departments": [department_id],
}
manager_result = managers.insert_one(manager_data)

print("Inserted data successfully!")
