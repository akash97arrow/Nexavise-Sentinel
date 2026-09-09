from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class SecurityEventCreate(BaseModel):
    event_type: str
    source_ip: str
    description: str
    severity: str


class SecurityEventResponse(BaseModel):
    id: int
    event_type: str
    source_ip: str
    description: str
    severity: str
    created_at: datetime        

    model_config = ConfigDict(from_attributes=True)