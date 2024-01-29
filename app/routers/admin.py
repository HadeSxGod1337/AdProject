from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from fastapi import Depends, HTTPException, status, APIRouter, Response


router = APIRouter()


@router.get('/')
def get_admin(db: Session = Depends(get_db), user: models.User = Depends(oauth2.require_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="access is denied")
    return user