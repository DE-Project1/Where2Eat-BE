from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import router
from fastapi.responses import FileResponse

app = FastAPI(title="Where2Eat BE")

origins = [
    "http://localhost:3000", "http://localhost:3001",
    "http://localhost:5173", "http://localhost:5174",
    "http://localhost:8000", "https://where2eat.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

@app.get("/", include_in_schema=False)
def root():
    return {"Where2Eat Server is running."}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")