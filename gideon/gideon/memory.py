"""
Tiered Memory Management Subsystem for Gideon Agentic OS.
Tier 1: Fast Working Memory (Volatile Process RAM)
Tier 2: Episodic Memory (Durable SQLite state)
Tier 3: Archival Storage (Virtual file system records)
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class MemorySubsystem:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._ram_pool: Dict[str, Any] = {}
        self._init_db()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS episodic_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pid INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_episodic_key ON episodic_memory(category, key);
            """)
            conn.commit()

    # Tier 1: Process RAM
    def ram_set(self, key: str, value: Any):
        self._ram_pool[key] = value

    def ram_get(self, key: str, default: Any = None) -> Any:
        return self._ram_pool.get(key, default)

    def ram_delete(self, key: str):
        self._ram_pool.pop(key, None)

    # Tier 2: Durable Episodic Memory
    def store_episodic(self, pid: int, category: str, key: str, value: Any):
        val_str = json.dumps(value) if not isinstance(value, str) else value
        now = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO episodic_memory (pid, category, key, value, created_at) VALUES (?, ?, ?, ?, ?)",
                (pid, category, key, val_str, now)
            )
            conn.commit()

    def query_episodic(self, category: Optional[str] = None, key: Optional[str] = None) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if category and key:
                cursor.execute("SELECT * FROM episodic_memory WHERE category = ? AND key = ? ORDER BY id DESC", (category, key))
            elif category:
                cursor.execute("SELECT * FROM episodic_memory WHERE category = ? ORDER BY id DESC", (category,))
            else:
                cursor.execute("SELECT * FROM episodic_memory ORDER BY id DESC LIMIT 50")
            
            results = []
            for row in cursor.fetchall():
                try:
                    parsed_val = json.loads(row["value"])
                except Exception:
                    parsed_val = row["value"]
                results.append({
                    "id": row["id"],
                    "pid": row["pid"],
                    "category": row["category"],
                    "key": row["key"],
                    "value": parsed_val,
                    "created_at": row["created_at"]
                })
            return results

    def get_stats(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM episodic_memory")
            count = cursor.fetchone()[0]
        return {
            "ram_keys_count": len(self._ram_pool),
            "episodic_records_count": count,
            "db_path": str(self.db_path)
        }
