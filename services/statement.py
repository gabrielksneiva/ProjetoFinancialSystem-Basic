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
    
    async def get_transaction_history(self, email: str,limit: int, page: int) -> list:
        transaction_history = await self.db.get_transaction_history(email, limit, page)
        if not transaction_history:
            raise HTTPException(status_code=404, detail="Transaction history not found")
        
        transactions_fetched = []
        for transaction in transaction_history:
            transactions_fetched.append({
                "transaction_id": transaction["transaction_id"],
                "amount": transaction["amount"],
                "transaction_type": transaction["transaction_type"],
                "created_at": transaction["created_at"],
                "updated_at": transaction["updated_at"]
            })
        
        return {"transactions": transactions_fetched}