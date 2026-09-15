from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    name: Mapped[str] = mapped_column(String(100))
    target: Mapped[str] = mapped_column(String(255))
    asset_type: Mapped[str] = mapped_column(String(50))
    authorization_status: Mapped[str] = mapped_column(
        String(20),
        default="AUTHORIZED"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))

    status: Mapped[str] = mapped_column(
        String(20),
        default="RUNNING"
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id")
    )

    scan_id: Mapped[int] = mapped_column(
        ForeignKey("scans.id")
    )

    port: Mapped[int] = mapped_column()

    protocol: Mapped[str] = mapped_column(
        String(20)
    )

    service: Mapped[str] = mapped_column(
        String(100)
    )

    state: Mapped[str] = mapped_column(
        String(20)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(primary_key=True)

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id")
    )

    scan_result_id: Mapped[int] = mapped_column(
        ForeignKey("scan_results.id")
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    severity: Mapped[str] = mapped_column(
        String(20)
    )

    risk_score: Mapped[int] = mapped_column()

    risk_level: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class FindingOccurrence(Base):
    __tablename__ = "finding_occurrences"

    id: Mapped[int] = mapped_column(primary_key=True)

    finding_id: Mapped[int] = mapped_column(
        ForeignKey("findings.id")
    )

    scan_id: Mapped[int] = mapped_column(
        ForeignKey("scans.id"),
        nullable=False
    )

    scan_result_id: Mapped[int] = mapped_column(
        ForeignKey("scan_results.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class AttackPath(Base):
    __tablename__ = "attack_paths"

    id: Mapped[int] = mapped_column(primary_key=True)

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id")
    )

    finding_id: Mapped[int] = mapped_column(
        ForeignKey("findings.id")
    )

    entry_point: Mapped[str] = mapped_column(
        String(100)
    )

    risk_score: Mapped[int] = mapped_column()

    risk_level: Mapped[str] = mapped_column(
        String(20)
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    event_type: Mapped[str] = mapped_column(
        String(100)
    )

    source_ip: Mapped[str] = mapped_column(
        String(50)
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    severity: Mapped[str] = mapped_column(
        String(20)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    event_id: Mapped[int] = mapped_column(
        ForeignKey("security_events.id")
    )

    risk_score: Mapped[int] = mapped_column()

    message: Mapped[str] = mapped_column(
        Text
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )