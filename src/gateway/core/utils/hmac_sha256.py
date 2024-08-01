import hashlib
import hmac


def hmac_digest(key: str, data: str) -> str:
    h = hmac.new(key.encode(), data.encode(), hashlib.sha256)
    digest = h.hexdigest()

    return digest
