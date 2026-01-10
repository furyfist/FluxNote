# FastAPI entry point for FluxNote Parser

from fastapi import FastAPI

app = FastAPI(title="FluxNote Parser API")


@app.get("/")
async def root():
    return {"message": "FluxNote Parser API is running"}
