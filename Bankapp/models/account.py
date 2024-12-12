from pydantic import BaseModel


class Account(BaseModel):
    account_id: int
    name: str
    balance: float


class UpdateAccount(BaseModel):
    name: str = None
    balance: float = None


class MoneyOperation(BaseModel):
    amount: float