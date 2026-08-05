from fastapi import FastAPI

from database import Base, engine
from routers import products

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Simple shop API",
    description="RESTful API for product managements.",
    version="0.1.0",
)


@app.get("/", tags=["default"])
def root():
    return {"status": "ok"}


app.include_router(products.router)
