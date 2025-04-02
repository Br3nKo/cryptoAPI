import httpx
import yaml
from fastapi import HTTPException
from pathlib import Path
from utils.utils import coingecko_map_result

config_path = Path(__file__).resolve().parent.parent / "coingecko_config.yml"
with config_path.open("r") as file:
    config = yaml.safe_load(file)

VS_CURRENCY = config['coingecko']['vs_currency']
COIN_EXISTS_URL = f"{config['coingecko']['coin_exists_url']}?vs_currency={VS_CURRENCY}"
GET_COIN_URL = config['coingecko']['get_coin_url']
GET_COIN_URL_QUERY = config['coingecko']['get_coin_url_query']


async def gecko_get_coins():
    """"get All coins from CoinGecko"""
    async with httpx.AsyncClient() as client:
        response = await client.get(COIN_EXISTS_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()
    

async def gecko_coin_exists(coin_symbol, coin_name):
    """ Verify the coin existence on CoinGecko """
    coins = await gecko_get_coins()
        
    for coin in coins:
        if coin['symbol'] == coin_symbol and coin['name'].lower() == coin_name.lower():
            return coingecko_map_result(coin, None)
    
    return None


async def gecko_get_coin_by_id(coin_id: str):
    """ Get coin data from CoinGecko """
    url = f"{GET_COIN_URL}/{coin_id}{GET_COIN_URL_QUERY}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        coin_data = response.json()
        
        if not coin_data:
            raise HTTPException(status_code=404, detail=f"Coin with ID '{coin_id}' not found.")
        
        coin_market = coin_data.get('market_data', {})
        return coingecko_map_result(coin_data, coin_market)
