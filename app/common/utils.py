import hashlib
import json
from datetime import datetime, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def stable_hash(payload: dict | list | str) -> str:
    if isinstance(payload, str):
        raw = payload
    else:
        raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
