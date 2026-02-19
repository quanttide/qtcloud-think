from fastapi import FastAPI

from api.v1 import clarify, meta, notes, workspace

app = FastAPI(title="qtcloud-think Provider API")

app.include_router(clarify.router, prefix="/api/v1")
app.include_router(notes.router, prefix="/api/v1")
app.include_router(workspace.router, prefix="/api/v1")
app.include_router(meta.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "qtcloud-think provider API"}


@app.get("/health")
def health():
    return {"status": "ok"}
