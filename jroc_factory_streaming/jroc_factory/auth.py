import asyncio, hashlib, hmac, os
from .schemas import AuthMessage

class AuthenticationError(Exception): pass

def configured_token() -> str:
    token = os.getenv("JROC_AUTH_TOKEN", "")
    if len(token) < 16:
        raise RuntimeError("JROC_AUTH_TOKEN must contain at least 16 characters")
    return token

async def authenticate(websocket) -> None:
    timeout = float(os.getenv("JROC_AUTH_TIMEOUT_SECONDS", "5"))
    try:
        raw = await asyncio.wait_for(websocket.recv(), timeout=timeout)
        msg = AuthMessage.model_validate_json(raw)
    except Exception as exc:
        raise AuthenticationError("invalid authentication message") from exc
    supplied = hashlib.sha256(msg.token.encode()).digest()
    expected = hashlib.sha256(configured_token().encode()).digest()
    if not hmac.compare_digest(supplied, expected):
        raise AuthenticationError("authentication failed")
