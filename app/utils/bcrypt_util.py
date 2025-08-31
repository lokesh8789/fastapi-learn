from passlib.context import CryptContext

context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_text(text: str) -> str:
    return context.hash(text)


def verify_text(plain_text: str, hashed_text: str) -> bool:
    return context.verify(plain_text, hashed_text)
