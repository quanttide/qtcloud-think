from fastapi import FastAPI

from app.api.v1 import clarify, organize, distill, meta

app = FastAPI(title="qtcloud-think Provider API")

app.include_router(clarify.router, prefix="/api/v1")
app.include_router(organize.router, prefix="/api/v1")
app.include_router(distill.router, prefix="/api/v1")
app.include_router(meta.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "qtcloud-think provider API"}


@app.get("/health")
def health():
    return {"status": "ok"}
