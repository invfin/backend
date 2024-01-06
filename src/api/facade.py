from collections import namedtuple
from datetime import datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings

from src.api.models import Jwt
from src.users.models import User

JWTPayload = namedtuple("JWTPayload", ["iss", "aud", "exp", "iat", "jti", "sub", "ref"])
JWTHeader = namedtuple("JWTHeader", ["typ", "alg"])
JWT = namedtuple("JWT", ["payload", "header"])


class JwtFacade:
    algorithm: str = "HS256"
    secret = settings.SECRET_KEY
    tokens: dict[str, str]
    audience: list[str] = ["frontend", "backend"]
    issuer = "inversionesyfinanzas.xyz"

    def __init__(self, now: datetime, user: Optional[User] = None) -> None:
        refresh_token, access_token = self.create_tokens(user, now)
        self.tokens = {
            "access": self.new(access_token, refresh_token.pk),
            "refresh": self.new(refresh_token, access_token.pk),
        }

    def create_tokens(self, user: Optional[User], date: datetime):
        # Sometimes it seems that the iat time fail, the token isn't ready.
        # Let's see if setting the exp date -1h less it syncs with the server time
        now = date - timedelta(hours=1)
        refresh_token = Jwt.objects.create(
            created_at=now,
            expiration_date=now + timedelta(days=29),
            user=user,
        )
        access_token = Jwt.objects.create(
            created_at=now,
            expiration_date=now + timedelta(days=1),
            user=user,
            refresh=refresh_token,
        )
        return refresh_token, access_token

    def get_payload(
        self,
        token: Jwt,
        related_token_id: int,
    ) -> JWTPayload:
        return JWTPayload(
            iss=self.issuer,
            aud=self.audience,
            exp=token.expiration_date.timestamp(),
            iat=token.created_at.timestamp(),
            jti=token.pk,
            sub=token.user.pk if token.user else "",
            ref=related_token_id,
        )

    def get_headers(self) -> JWTHeader:
        return JWTHeader(typ="JWT", alg=self.algorithm)

    def new(self, token: Jwt, related_token_id: int) -> str:
        return jwt.encode(
            self.get_payload(token, related_token_id)._asdict(),
            self.secret,
            algorithm=self.algorithm,
            headers=self.get_headers()._asdict(),
        )

    @classmethod
    def decode(cls, token: str) -> JWTPayload:
        payload = jwt.decode(
            token,
            cls.secret,
            algorithms=[cls.algorithm],
            options={"require": ["exp", "iss", "sub"]},  # TODO: check, it doesn0t seem right
            audience=cls.audience,
            issuer=cls.issuer,
        )
        return JWTPayload(**payload)
