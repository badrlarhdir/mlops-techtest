import jwt
import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler:
    """
    This class handles the authentication operations such as password hashing, token encoding and decoding,
    and token verification.
    """

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.getenv("SECRET_KEY", "SECRET")

    def get_password_hash(self, password):
        """
        This method takes a plain password, hashes it and returns the hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """
        This method takes a plain password and a hashed password, verifies the plain password against the hashed password
        and returns True if they match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        """
        This method takes a user_id, encodes it into a JWT along with the expiration and issued at times,
        and returns the encoded token.
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=15),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        """
        This method takes a token, decodes it, and returns the user_id from the payload.
        If the token is expired or invalid, it raises an HTTPException.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """
        This method is a wrapper for the decode_token method. It takes an HTTPAuthorizationCredentials object,
        extracts the token from it, and passes it to the decode_token method.
        """
        return self.decode_token(auth.credentials)
