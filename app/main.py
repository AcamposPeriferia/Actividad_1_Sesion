from fastapi import FastAPI

from app.api.transfers import router as transfers_router

app = FastAPI(title="Mini Bank API", version="1.0.0")
app.include_router(transfers_router)


@app.get("/")
def health_check():
    return {"message": "Mini Bank API is running"}
