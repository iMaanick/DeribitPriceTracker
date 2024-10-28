from pydantic import BaseModel, Field, ConfigDict


class CryptoPrice(BaseModel):
    ticker: str = Field(..., title="Ticker", example="btc_usd")
    price: float = Field(..., title="Price", example=50000.00)
    timestamp: int = Field(..., title="Timestamp in UNIX format", example=1633116800)
    model_config = ConfigDict(from_attributes=True)
