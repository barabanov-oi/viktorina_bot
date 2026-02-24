from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class RateEntry:
    count: int
    expires_at: datetime


class InMemoryRateLimiter:
    def __init__(self, limit: int, window_seconds: int, max_keys: int = 10000):
        self.limit = limit
        self.window_seconds = window_seconds
        self.max_keys = max_keys
        self._store: OrderedDict[str, RateEntry] = OrderedDict()

    def allow(self, key: str) -> bool:
        now = datetime.now(timezone.utc)
        entry = self._store.get(key)
        if entry is None or entry.expires_at <= now:
            self._store[key] = RateEntry(count=1, expires_at=now + timedelta(seconds=self.window_seconds))
            self._store.move_to_end(key)
            self._trim()
            return True
        if entry.count >= self.limit:
            return False
        entry.count += 1
        self._store.move_to_end(key)
        return True

    def _trim(self) -> None:
        while len(self._store) > self.max_keys:
            self._store.popitem(last=False)
