from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies.core import DBSessionDep
from sqlalchemy.future import select
from app.database import get_db_session
from app.schemas.coin import CoinCreate, CoinResponse, CoinsResponse
from app.crud.coin import *

router = APIRouter()


@router.post("/coin/", response_model=CoinResponse)
async def create_coin(coin: CoinCreate, db: DBSessionDep):
    """
    Add Coin using its symbol and name
    """
    return await create_coin_by_symbol_and_name(coin.symbol, coin.name, db)


@router.get("/coin/{id}", response_model=CoinResponse)
async def get_coin(id: str, db: DBSessionDep):
    """
    Retrieve Coin by ID
    """
    return await get_coin_by_id(id, db)


@router.get("/coins", response_model=CoinsResponse)
async def get_coins(db: DBSessionDep):
    """
    Retrieve all the coins
    """
    coins = await get_all_coins(db)
    coin_responses = [CoinResponse(**coin.__dict__) for coin in coins]
    return CoinsResponse(coins=coin_responses)


@router.put("/coin/{coin_id}", response_model=CoinResponse)
async def update_coin(coin_id: str, db: DBSessionDep):
    """
    Update coin by ID with CoinGecko data
    """
    return await update_coin_by_id(coin_id, db)


@router.put("/coins", response_model=None)
async def update_coins(db: DBSessionDep):
    """
    Update all the coins with CoinGecko data
    """
    return await update_all_coins(db)


@router.delete("/coin/{coin_id}", response_model=None)
async def delete_coin(coin_id: str, db: DBSessionDep):
    """
    Delete Coin by ID
    """
    return await delete_coin_by_id(coin_id, db)
