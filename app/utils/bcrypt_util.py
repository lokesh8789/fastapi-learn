import bcrypt

def hash_text(text: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(text.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_text(plain_text: str, hashed_text: str) -> bool:
    return bcrypt.checkpw(plain_text.encode("utf-8"), hashed_text.encode("utf-8"))
