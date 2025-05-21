from repositories.database import Database
from fastapi import HTTPException


class DepositService:
    def __init__(self, db: Database):
        self.db = db

    async def deposit(self, email: str, amount: float):
        create_deposit_on_db = await self.db.create_deposit(email=email, amount=amount)
        if not create_deposit_on_db:
            raise HTTPException(status_code=400, detail="Deposit failed")
        
        response = {
            "message": "Deposit successful",
            "transaction_id": create_deposit_on_db.get("transaction_id"),
        }
        
        return response