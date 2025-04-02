from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

from database import Base

class Coin(Base):
    __tablename__ = "coins"

    id: Mapped[str] = mapped_column(primary_key=True, index=True, unique=True)
    symbol: Mapped[str] = mapped_column(index=True)
    name: Mapped[str]
    current_price: Mapped[float]
    market_cap: Mapped[float]
    total_volume: Mapped[float]
    circulating_supply: Mapped[float]
    high_24h: Mapped[float]
    low_24h: Mapped[float]
    last_updated: Mapped[datetime] = mapped_column(default=datetime.now())

    def __repr__(self) -> str:
        return f"<Coin(name={self.name}, symbol={self.symbol}, price={self.current_price})>"
