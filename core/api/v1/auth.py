import secrets
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from ninja.security import HttpBearer


class SecretKeyAuth(HttpBearer):
    def authenticate(
        self,
        request: HttpRequest,
        token: str | None,
    ) -> Any | None:
        if secrets.compare_digest(token, settings.DJANGO_API_SECRET_KEY):
            return True

        return None
