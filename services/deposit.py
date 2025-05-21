from repositories.database import Database
from fastapi import HTTPException


class DepositService:
    def __init__(self, db: Database):
        self.db = db

    def deposit(self, email: str, amount: float):
        create_deposit_on_db = self.db.create_deposit(email=email, amount=amount)
        if not create_deposit_on_db:
            raise HTTPException(status_code=400, detail="Deposit failed")
        
        return create_deposit_on_db