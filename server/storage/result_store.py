import threading
import time
from typing import Any

from server.config import settings


class ResultStore:
    def __init__(self, ttl: int | None = None):
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()
        self._ttl = ttl or settings.result_ttl

    def put(self, result_id: str, data: Any) -> None:
        with self._lock:
            self._store[result_id] = (data, time.time())

    def get(self, result_id: str) -> Any | None:
        with self._lock:
            entry = self._store.get(result_id)
            if entry is None:
                return None
            data, ts = entry
            if time.time() - ts > self._ttl:
                del self._store[result_id]
                return None
            return data

    def delete(self, result_id: str) -> bool:
        with self._lock:
            return self._store.pop(result_id, None) is not None

    def list_ids(self) -> list[str]:
        with self._lock:
            now = time.time()
            return [
                rid for rid, (_, ts) in self._store.items()
                if now - ts <= self._ttl
            ]

    def purge_expired(self) -> int:
        with self._lock:
            now = time.time()
            expired = [rid for rid, (_, ts) in self._store.items() if now - ts > self._ttl]
            for rid in expired:
                del self._store[rid]
            return len(expired)


result_store = ResultStore()
