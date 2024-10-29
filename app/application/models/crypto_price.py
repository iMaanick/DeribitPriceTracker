from pydantic import BaseModel, Field, ConfigDict


class CryptoPrice(BaseModel):
    id: int = Field(title="ID", examples=[1])
    ticker: str = Field(title="Ticker", examples=["btc_usd"])
    price: float = Field(title="Price", examples=[50000.00])
    timestamp: int = Field(title="Timestamp in UNIX format", examples=[1633116800])
    model_config = ConfigDict(from_attributes=True)


class CryptoPriceCreate(BaseModel):
    ticker: str = Field(title="Ticker", examples=["btc_usd"])
    price: float = Field(title="Price", examples=[50000.00])
    timestamp: int = Field(title="Timestamp in UNIX format", examples=[1633116800])
