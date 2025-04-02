from fastapi import FastAPI
from app.api.routes.router import router
from fastapi.middleware.cors import CORSMiddleware
from app.database import sessionmanager
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger 
import asyncio
import httpx


async def schedule_coin_updates():
    """
    Calls PUT request to update the coins in the database
    """
    async with httpx.AsyncClient() as client:
        await client.put("http://localhost:8000/coins") 

def start_scheduler():
    """
    Starts the update function in the background.
    """
    asyncio.run(schedule_coin_updates())


scheduler = BackgroundScheduler()
trigger = IntervalTrigger(minutes=1)
scheduler.add_job(start_scheduler, trigger)
scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan,)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get("/")
async def index():
    return {"message": "FastAPI server is running"}
