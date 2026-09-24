from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.accounts import router as accounts_router
from app.api.audit import router as audit_router
from app.api.transfers import router as transfers_router

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="Mini Bank API", version="2.0.0")
app.include_router(accounts_router)
app.include_router(transfers_router)
app.include_router(audit_router)


@app.get("/health")
def health_check():
    return {"message": "Mini Bank API is running"}


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/app/")


app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
