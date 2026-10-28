import hashlib, json, sqlite3, threading
from datetime import datetime, timezone

class AuditStore:
    def __init__(self, path: str):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.Lock()
        self.db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, at TEXT NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL, previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL UNIQUE)")
        self.db.execute("CREATE TABLE IF NOT EXISTS assets (asset_id TEXT PRIMARY KEY, state TEXT NOT NULL, payload TEXT NOT NULL)")
        self.db.commit()

    def append(self, kind: str, payload: dict) -> str:
        with self.lock:
            row=self.db.execute("SELECT event_hash FROM events ORDER BY id DESC LIMIT 1").fetchone()
            previous=row[0] if row else "GENESIS"
            at=datetime.now(timezone.utc).isoformat()
            body=json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
            digest=hashlib.sha256(f"{previous}|{at}|{kind}|{body}".encode()).hexdigest()
            self.db.execute("INSERT INTO events(at,kind,payload,previous_hash,event_hash) VALUES(?,?,?,?,?)", (at,kind,body,previous,digest))
            self.db.commit(); return digest

    def put_asset(self, asset_id: str, state: str, payload: dict):
        body=json.dumps(payload, sort_keys=True, default=str)
        self.db.execute("INSERT INTO assets VALUES(?,?,?) ON CONFLICT(asset_id) DO UPDATE SET state=excluded.state,payload=excluded.payload", (asset_id,state,body)); self.db.commit()

    def get_asset(self, asset_id: str):
        row=self.db.execute("SELECT state,payload FROM assets WHERE asset_id=?", (asset_id,)).fetchone()
        return None if not row else {"state":row[0], "payload":json.loads(row[1])}

    def list_assets(self):
        return [{"asset_id":r[0],"state":r[1]} for r in self.db.execute("SELECT asset_id,state FROM assets ORDER BY asset_id")]
