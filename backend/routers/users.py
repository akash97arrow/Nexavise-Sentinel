from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from backend.database import get_db
from backend.models import User
from backend.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    LoginRequest,
)
from backend.auth import create_access_token
from backend.dependencies import get_current_user


router = APIRouter()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# GET /users
# Protected route
# Returns only the currently authenticated user.

@router.get(
    "/users",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    user = (
        db.query(User)
        .filter(User.id == current_user)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return [user]


# GET /users/{user_id}
# Users can only access their own account.

@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    if user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    user = (
        db.query(User)
        .filter(User.id == current_user)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


# POST /users
# Register new user.

@router.post(
    "/users",
    response_model=UserResponse,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        hashed_password = pwd_context.hash(
            user.password
        )

        new_user = User(
            name=user.name.strip(),
            email=user.email.strip().lower(),
            password_hash=hashed_password,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )


# PUT /users/{user_id}
# Users can only update their own account.

@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    if user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    existing_user = (
        db.query(User)
        .filter(User.id == current_user)
        .first()
    )

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    existing_user.name = user.name.strip()
    existing_user.email = user.email.strip().lower()

    try:
        db.commit()
        db.refresh(existing_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    return existing_user


# DELETE /users/{user_id}
# Users can only delete their own account.

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    if user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    user = (
        db.query(User)
        .filter(User.id == current_user)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully",
    }


# POST /login
# Login and generate JWT.

@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db),
):
    email = user.email.strip().lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not pwd_context.verify(
        user.password,
        existing_user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        existing_user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }