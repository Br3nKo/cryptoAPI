import os
from datetime import datetime

def get_url():
    return os.getenv("DATABASE_URL")


def coingecko_map_result(coin, market_data):
    mapped_coin = {
        "id": coin.get('id'),
        "symbol": coin.get('symbol'),
        "name": coin.get('name'),
        "current_price": coin.get('current_price'),
        "market_cap": coin.get('market_cap'),
        "total_volume": coin.get('total_volume'),
        "circulating_supply": coin.get('circulating_supply'),
        "high_24h": coin.get('high_24h'),
        "low_24h": coin.get('low_24h'),
        "last_updated": datetime.strptime(coin.get('last_updated', datetime.now().isoformat()), "%Y-%m-%dT%H:%M:%S.%fZ")
    }

    if market_data:
        for key in ["current_price", "market_cap", "total_volume", "high_24h", "low_24h"]:
            mapped_coin[key] = market_data.get(key, {}).get("eur", mapped_coin[key])

    return mapped_coin


def update_db_coin(db_coin, coin_data):
    db_coin.name = coin_data['name']
    db_coin.symbol = coin_data['symbol']
    db_coin.current_price = coin_data['current_price']
    db_coin.market_cap = coin_data['market_cap']
    db_coin.total_volume = coin_data['total_volume']
    db_coin.high_24h = coin_data['high_24h']
    db_coin.low_24h = coin_data['low_24h']
    db_coin.last_updated = coin_data['last_updated']

    return None
