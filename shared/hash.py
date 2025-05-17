import bcrypt

def hash_any_string(self, any_string: str) -> str:
        # Hash any string using bcrypt
        hashed_any_string = bcrypt.hashpw(any_string.encode('utf-8'), bcrypt.gensalt())
        return hashed_any_string.decode('utf-8')