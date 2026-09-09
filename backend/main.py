from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.routers.users import router as users_router
from backend.routers.events import router as events_router


app = FastAPI(title="Nexavise Sentinel API")

app.include_router(events_router)
app.include_router(users_router)


@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    return {
        "status": "ok",
        "message": "SQLAlchemy database session is working"
    }