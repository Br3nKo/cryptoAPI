from datetime import datetime
from models.coin import Coin
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from services.coingecko import gecko_coin_exists, gecko_get_coin_by_id, gecko_get_coins
from utils.utils import update_db_coin


async def create_coin_by_symbol_and_name(symbol: str, name: str, db: AsyncSession):
    """ Creates new Coin in the db """
    try:
        coingecko_response = await gecko_coin_exists(symbol, name)

        if not coingecko_response:
            raise HTTPException(status_code=404, detail="Coin not found on CoinGecko")

        db_coin = Coin(**coingecko_response)
        db.add(db_coin)
        await db.flush()
        await db.commit()
        await db.refresh(db_coin)
        return db_coin

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


async def get_coin_by_id(id: str, db: AsyncSession):
    """ Retrieves a Coin from db by ID """
    coin = (await db.scalars(select(Coin).where(Coin.id == id))).first()

    if not coin:
        raise HTTPException(status_code=404, detail="Coin not found")
    
    return coin


async def get_all_coins(db: AsyncSession):
    """ Retrieves all Coins from db """
    coins = (await db.scalars(select(Coin))).all()
    return coins


async def update_coin_by_id(id: str, db: AsyncSession):
    """ Updates a Coin in db by ID """
    db_coin = (await db.scalars(select(Coin).where(Coin.id == id))).first()

    if not db_coin:
        raise HTTPException(status_code=404, detail=f"Coin with ID '{id}' not found.")
    
    coingecko_response = await gecko_get_coin_by_id(id)
    if not coingecko_response:
        raise HTTPException(status_code=404, detail="Coin not found on CoinGecko")
    
    update_db_coin(db_coin, coingecko_response)
    
    await db.commit()
    await db.refresh(db_coin)
    return db_coin


async def update_all_coins(db: AsyncSession):
    """
    Updates all coins in the database with the latest data from CoinGecko.
    """
    db_coins = (await db.scalars(select(Coin))).all()

    if not db_coins:
        return {"message": "No coins found in the database"}

    coingecko_coins = await gecko_get_coins()
    if not coingecko_coins:
        raise HTTPException(status_code=500, detail="Failed to fetch data from CoinGecko")

    coingecko_dict = {coin["id"]: coin for coin in coingecko_coins}

    for db_coin in db_coins:
        if db_coin.id in coingecko_dict:
            coin_data = coingecko_dict[db_coin.id]
            update_db_coin(db_coin, coin_data)
            db_coin.last_updated = datetime.fromisoformat(coin_data["last_updated"].replace("Z", "+00:00")).replace(tzinfo=None)

    await db.commit()
    return {"message": "All coins updated successfully"}


async def delete_coin_by_id(id: str, db: AsyncSession):
    """ Deletes a Coin from db by ID """
    db_coin = (await db.scalars(select(Coin).where(Coin.id == id))).first()

    if not db_coin:
        raise HTTPException(status_code=404, detail=f"Coin with ID '{id}' not found.")
    
    await db.delete(db_coin)
    await db.commit()
    return {"message": f"Coin with ID: {id} deleted successfully"}
