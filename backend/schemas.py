from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class AssetCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )

    target: str = Field(
        min_length=1,
        max_length=255
    )

    asset_type: str = Field(
        min_length=1,
        max_length=50
    )

    authorization_status: str = Field(
        min_length=1,
        max_length=20
    )

    @field_validator(
        "name",
        "target",
        "asset_type",
        "authorization_status"
    )
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty")

        return value


class AssetResponse(BaseModel):
    id: int
    name: str
    target: str
    asset_type: str
    authorization_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SecurityEventCreate(BaseModel):
    event_type: str = Field(min_length=1, max_length=100)
    source_ip: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=1000)
    severity: str = Field(min_length=1, max_length=20)

    @field_validator(
        "event_type",
        "source_ip",
        "description",
        "severity",
    )
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty")

        return value

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: str) -> str:
        value = value.upper()

        allowed = {
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        }

        if value not in allowed:
            raise ValueError(
                "Severity must be LOW, MEDIUM, HIGH, or CRITICAL"
            )

        return value


class SecurityEventResponse(BaseModel):
    id: int
    event_type: str
    source_ip: str
    description: str
    severity: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertResponse(BaseModel):
    id: int
    event_id: int
    risk_score: int
    message: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=20)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.strip().upper()

        if value not in ("OPEN", "RESOLVED"):
            raise ValueError(
                "Status must be OPEN or RESOLVED"
            )

        return value


class FindingResponse(BaseModel):
    id: int
    asset_id: int
    scan_result_id: int
    title: str
    description: str
    severity: str
    risk_score: int
    risk_level: str | None
    status: str
    created_at: datetime
    last_seen_scan_id: int | None = None
    occurrence_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class FindingOccurrenceResponse(BaseModel):
    id: int
    finding_id: int
    scan_id: int
    scan_result_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FindingUpdate(BaseModel):
    status: str


class ScanResponse(BaseModel):
    id: int
    asset_id: int
    status: str
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ScanResultResponse(BaseModel):
    id: int
    asset_id: int
    scan_id: int | None
    port: int
    protocol: str
    service: str
    state: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttackPathResponse(BaseModel):
    id: int
    asset_id: int
    finding_id: int
    entry_point: str
    risk_score: int
    risk_level: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttackPathUpdate(BaseModel):
    status: str