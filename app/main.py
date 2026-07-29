from fastapi import FastAPI

app = FastAPI(
    title="Intelligent Cloud Storage Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Cloud Storage Platform is running."
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }