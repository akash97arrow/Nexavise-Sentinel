from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import AttackPath, Asset
from backend.schemas import AttackPathResponse, AttackPathUpdate
from backend.dependencies import get_current_user


router = APIRouter()


@router.get(
    "/attack-paths",
    response_model=list[AttackPathResponse],
)
def get_attack_paths(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    attack_paths = (
        db.query(AttackPath)
        .join(
            Asset,
            AttackPath.asset_id == Asset.id,
        )
        .filter(
            Asset.user_id == current_user
        )
        .order_by(
            AttackPath.risk_score.desc()
        )
        .all()
    )

    return attack_paths


@router.get(
    "/attack-paths/{attack_path_id}",
    response_model=AttackPathResponse,
)
def get_attack_path(
    attack_path_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    attack_path = (
        db.query(AttackPath)
        .join(
            Asset,
            AttackPath.asset_id == Asset.id,
        )
        .filter(
            AttackPath.id == attack_path_id,
            Asset.user_id == current_user,
        )
        .first()
    )

    if attack_path is None:
        raise HTTPException(
            status_code=404,
            detail="Attack path not found",
        )

    return attack_path


@router.patch(
    "/attack-paths/{attack_path_id}",
    response_model=AttackPathResponse,
)
def update_attack_path(
    attack_path_id: int,
    update: AttackPathUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    attack_path = (
        db.query(AttackPath)
        .join(
            Asset,
            AttackPath.asset_id == Asset.id,
        )
        .filter(
            AttackPath.id == attack_path_id,
            Asset.user_id == current_user,
        )
        .first()
    )

    if attack_path is None:
        raise HTTPException(
            status_code=404,
            detail="Attack path not found",
        )

    status = update.status.strip().upper()

    if status not in ("OPEN", "RESOLVED"):
        raise HTTPException(
            status_code=400,
            detail="Status must be OPEN or RESOLVED",
        )

    attack_path.status = status

    db.commit()
    db.refresh(attack_path)

    return attack_path