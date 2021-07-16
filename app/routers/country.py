from fastapi import APIRouter, HTTPException, Response, status, Depends
import schemas, models, database, helper
from sqlalchemy.orm import Session

router = APIRouter(
    tags = ['Country List']
)


# Get full list of country names
@router.get("/countrylist", status_code=status.HTTP_200_OK)
async def get_country_list(db: Session = Depends(database.get_db)):
    results = db.query(models.Country).all()
    return results