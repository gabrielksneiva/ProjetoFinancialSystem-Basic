from repositories.database import Database
from fastapi import HTTPException
from decimal import Decimal


class WithdrawService:
    def __init__(self, db: Database):
        self.db = db

    async def create(self, email: str, amount: float):
        aveilable_balance = await self.db.get_balance(email=email)
        if not aveilable_balance:
            raise HTTPException(status_code=404, detail="User not found")
        
        if aveilable_balance.get("balance") < Decimal(str(amount)):
            raise HTTPException(status_code=400, detail="Insufficient balance")
        
        create_withdraw_on_db = await self.db.create_withdraw(email=email, amount=amount)
        if not create_withdraw_on_db:
            raise HTTPException(status_code=400, detail="withdraw failed")
        
        response = {
            "message": "Withdraw successful",
            "transaction_id": create_withdraw_on_db.get("transaction_id"),
        }
        
        return response