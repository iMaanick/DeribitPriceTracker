from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped

from app.adapters.sqlalchemy_db.models import Base


class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)