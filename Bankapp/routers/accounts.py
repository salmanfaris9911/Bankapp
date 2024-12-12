from fastapi import APIRouter, HTTPException
from typing import List
from models.account import Account, UpdateAccount, MoneyOperation
from db.database import accounts_db


router = APIRouter(prefix="/accounts", tags=["Accounts"])


# Create a new account
@router.post("/", response_model=Account)
def create_account(account: Account):
    if account.account_id in accounts_db:
        raise HTTPException(status_code=400, detail="Account already exists")
    accounts_db[account.account_id] = account
    return account


# Get details of an account
@router.get("/{account_id}", response_model=Account)
def get_account(account_id: int):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts_db[account_id]


# Get all accounts
@router.get("/", response_model=List[Account])
def list_accounts():
    return list(accounts_db.values())


# Update account details
@router.put("/{account_id}", response_model=Account)
def update_account(account_id: int, updates: UpdateAccount):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")


    account = accounts_db[account_id]


    if updates.name is not None:
        account.name = updates.name
    if updates.balance is not None:
        account.balance = updates.balance


    accounts_db[account_id] = account
    return account


# Delete an account
@router.delete("/{account_id}", response_model=dict)
def delete_account(account_id: int):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")


    del accounts_db[account_id]
    return {"message": "Account deleted successfully"}


# Deposit money into an account
@router.post("/{account_id}/deposit", response_model=Account)
def deposit_money(account_id: int, operation: MoneyOperation):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")


    if operation.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")


    account = accounts_db[account_id]
    account.balance += operation.amount
    accounts_db[account_id] = account
    return account


# Withdraw money from an account
@router.post("/{account_id}/withdraw", response_model=Account)
def withdraw_money(account_id: int, operation: MoneyOperation):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")


    if operation.amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")


    account = accounts_db[account_id]


    if account.balance < operation.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")


    account.balance -= operation.amount
    accounts_db[account_id] = account
    return account
