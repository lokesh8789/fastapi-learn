import jwt
from datetime import datetime, timedelta, timezone
from typing import Any

# Normally pulled from config / env
SECRET_KEY = "fastship-world-class-project"  # 🔑 use env var in real app
ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 5 * 60  # 5 hours


class JwtUtil:
    @staticmethod
    def generate_token(
        username: str, extra_claims: dict[str, Any] | None = None
    ) -> str:
        """
        Generate JWT token for given username (subject).
        """
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=JWT_EXPIRATION_MINUTES)

        payload = {
            "sub": username,
            "iat": now,  # issued at
            "exp": expire,  # expiration
        }
        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def get_claims_from_token(token: str) -> dict[str, Any] | None:
        """
        Parse all claims from JWT token.
        """
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def get_username_from_token(token: str) -> str | None:
        """
        Extract username (subject) from token.
        """
        claims = JwtUtil.get_claims_from_token(token)
        if claims:
            return claims.get("sub")
        return None

    @staticmethod
    def is_token_expired(token: str) -> bool:
        """
        Check if the token is expired.
        """
        claims = JwtUtil.get_claims_from_token(token)
        if not claims:
            return True
        exp: int | None = claims.get("exp")
        if not exp:
            return True
        return datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc)

    @staticmethod
    def validate_token(token: str, username: str) -> bool:
        """
        Validate token: correct username and not expired.
        """
        extracted_username = JwtUtil.get_username_from_token(token)
        return extracted_username == username and not JwtUtil.is_token_expired(
            token
        )
