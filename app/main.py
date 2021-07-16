from fastapi import FastAPI
from routers import summary, daily, country
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(summary.router)
app.include_router(daily.router)
app.include_router(country.router)

# Landing Page
@app.get("/")
def root():
    return {"message": "Welcome to Covid API Landing Page!"}
