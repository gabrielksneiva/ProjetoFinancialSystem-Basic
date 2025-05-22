from fastapi import HTTPException
from repositories.database import Database


class StatementService:
    def __init__(self, db: Database):
        self.db = db

    async def get_balance(self, email: str) -> dict:
        balance_fetched = await self.db.get_balance(email=email)
        if not balance_fetched:
            raise HTTPException(status_code=404, detail="Balance not found")

        return {"balance": balance_fetched["balance"]}
    
    async def get_transaction_history(self, email: str) -> list:
        

        return result