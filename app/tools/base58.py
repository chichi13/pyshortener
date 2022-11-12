import random

from app.core.config import settings


def human_readable_string() -> str:
    base58_string = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return "".join(random.choices(base58_string, k=settings.SHORT_CODE_LENGTH))
