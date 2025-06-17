from fastapi import FastAPI

app = FastAPI(
    title="Restaurant Review NLP Service",
)

@app.get("/healthz")
async def healthz():
    """
    Health check endpoint verifying the service is up.
    Returns 200 OK if the app is running.
    """
    return {"status": "ok"}