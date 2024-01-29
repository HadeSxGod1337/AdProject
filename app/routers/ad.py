from datetime import datetime
import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from app.oauth2 import require_user

router = APIRouter()


@router.get('/', response_model=schemas.ListAdResponse)
def get_ads(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '', user: models.User = Depends(require_user)):
    skip = (page - 1) * limit

    ads = db.query(models.Ad).group_by(models.Ad.id).filter(
        models.Ad.title.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(ads), 'ads': ads}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.AdResponse)
def create_ad(ad: schemas.CreateAdSchema, db: Session = Depends(get_db), user: models.User = Depends(require_user)):
    ad.user_id = uuid.UUID(user.id).hex if ad.user_id is None else ad.user_id.hex
    new_ad = models.Ad(**ad.dict())
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    return new_ad

@router.put('/{id}', response_model=schemas.AdResponse)
def update_ad(id: str, ad: schemas.UpdateAdSchema, db: Session = Depends(get_db), user: models.User = Depends(require_user)):
    ad_query = db.query(models.Ad).filter(models.Ad.id == id)
    updated_ad = ad_query.first()

    if not updated_ad:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No ad with this id: {id} found')
    if updated_ad.user_id != user.id or not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    ad.user_id = user.id
    ad_query.update(ad.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_ad

@router.get('/{id}', response_model=schemas.AdResponse)
def get_ad(id: str, db: Session = Depends(get_db), user: models.User = Depends(require_user)):
    ad = db.query(models.Ad).filter(models.Ad.id == id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No ad with this id: {id} found")
    return ad

@router.delete('/{id}')
def delete_ad(id: str, db: Session = Depends(get_db), user: models.User = Depends(require_user)):
    ad_query = db.query(models.Ad).filter(models.Ad.id == id)
    ad = ad_query.first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No ad with this id: {id} found')

    if ad.user_id != user.id or not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    ad_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)