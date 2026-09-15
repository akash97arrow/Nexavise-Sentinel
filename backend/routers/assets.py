from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Asset
from backend.schemas import AssetCreate, AssetResponse
from backend.dependencies import get_current_user

router = APIRouter()


@router.post("/assets", response_model=AssetResponse)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    if asset.authorization_status.upper() != "AUTHORIZED":
        raise HTTPException(
            status_code=400,
            detail="Asset must be explicitly authorized before scanning",
        )

    new_asset = Asset(
        user_id=current_user,
        name=asset.name,
        target=asset.target,
        asset_type=asset.asset_type,
        authorization_status=asset.authorization_status.upper(),
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


@router.get("/assets", response_model=list[AssetResponse])
def get_assets(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    assets = (
        db.query(Asset)
        .filter(Asset.user_id == current_user)
        .order_by(Asset.created_at.desc())
        .all()
    )

    return assets
