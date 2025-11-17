from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class RefreshTokenData(BaseModel):
    refresh_token: str | None = None


class TokenData(BaseModel):
    username: str | None = None
