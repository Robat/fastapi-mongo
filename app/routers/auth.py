from fastapi import APIRouter, Depends, HTTPException
from app.config.auth import create_custom_jwt_auth
from app.schemas.user import UserCreate as UserCreateSchema
from app.models.user import UserCreate as UserCreateModel
from app.database.connection import get_db_client
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import get_settings

router = APIRouter()


@router.post("/register", tags=["Authentication"])
async def register(user: UserCreateModel, db_client: AsyncIOMotorClient = Depends(get_db_client)):
    # Hash password before saving to database
    # Replace with a secure hashing method, e.g., bcrypt
    hashed_password = user.password
    user_in_db = UserCreateSchema(
        email=user.email, hashed_password=hashed_password)

    # Save user to MongoDB
    result = await db_client[get_settings().MONGODB_DATABASE_NAME]["users"].insert_one(user_in_db.dict())
    if not result.acknowledged:
        raise HTTPException(
            status_code=400, detail="Error occurred while registering user")

    return {"message": "User registered successfully"}


@router.post("/login", tags=["Authentication"])
async def login(user: UserCreateModel, db_client: AsyncIOMotorClient = Depends(get_db_client)):
    # Find user in the database
    user_in_db = await db_client[get_settings().MONGODB_DATABASE_NAME]["users"].find_one({"email": user.email})

    if not user_in_db:
        raise HTTPException(
            status_code=401, detail="Invalid email or password")
    # Verify password
    # Replace with a secure password verification method, e.g., bcrypt
    is_valid_password = user.password == user_in_db["hashed_password"]

    if not is_valid_password:
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

    # Create JWT access token
    jwt = create_custom_jwt_auth()
    access_token = jwt.create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "Bearer"}
