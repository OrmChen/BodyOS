"""
BODYOS — Unified Storage
Supabase-first with automatic local JSON fallback.
Credentials: .env (local dev) → st.secrets (Streamlit Cloud)
"""
import json
import uuid
import os
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv

# Load .env for local development
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ============================================
# Credential loading
# ============================================
def _get_credentials():
    """Load Supabase credentials — .env first, then st.secrets (Streamlit Cloud)."""
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")

    # Streamlit Cloud secrets take precedence
    try:
        import streamlit as st
        if st.secrets.get("SUPABASE_URL"):
            url = st.secrets["SUPABASE_URL"]
        if st.secrets.get("SUPABASE_KEY"):
            key = st.secrets["SUPABASE_KEY"]
    except Exception:
        pass

    return url, key


# ============================================
# Supabase client (lazy init)
# ============================================
_supabase = None
_supabase_available = None  # None=unchecked, True=available, False=unavailable


def _get_supabase_client():
    """Return raw Supabase client or None."""
    global _supabase
    if _supabase is not None:
        return _supabase

    url, key = _get_credentials()
    if not url or not key or "your-project" in url:
        return None

    try:
        from supabase import create_client
        _supabase = create_client(url, key)
        return _supabase
    except Exception:
        return None


def check_connection():
    """
    Test Supabase connection.
    Returns (connected: bool, message: str).
    """
    global _supabase_available

    url, key = _get_credentials()

    if not url or not key or "your-project" in url:
        _supabase_available = False
        return False, "未配置 Supabase 凭证"

    client = _get_supabase_client()
    if client is None:
        _supabase_available = False
        return False, "Supabase 客户端初始化失败"

    try:
        client.table("workouts").select("id").limit(1).execute()
        _supabase_available = True
        return True, "云端同步"
    except Exception as e:
        _supabase_available = False
        msg = str(e)[:80]
        return False, f"连接失败: {msg}"


def is_cloud_connected():
    """Quick cached check — has Supabase been confirmed reachable?"""
    if _supabase_available is None:
        check_connection()
    return _supabase_available is True


# ============================================
# Local JSON fallback
# ============================================
def _json_encoder(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Unserializable: {type(obj)}")


def _local_load(name):
    path = DATA_DIR / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def _local_save(name, data):
    (DATA_DIR / f"{name}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=_json_encoder),
        encoding="utf-8",
    )


# ============================================
# Query result wrapper
# ============================================
class Result:
    def __init__(self, data, count=None):
        self.data = data
        self.count = count if count is not None else len(data)


# ============================================
# Local table query (Supabase-compatible API)
# ============================================
class Query:
    def __init__(self, table_name):
        self.table_name = table_name
        self._filters = []
        self._order_col = None
        self._order_desc = False
        self._limit_val = None
        self._insert_data = None
        self._do_delete = False

    def select(self, cols="*", **kw):
        return self

    def eq(self, col, value):
        self._filters.append(("eq", col, value))
        return self

    def gte(self, col, value):
        self._filters.append(("gte", col, str(value)))
        return self

    def lte(self, col, value):
        self._filters.append(("lte", col, str(value)))
        return self

    def order(self, col, desc=False):
        self._order_col = col
        self._order_desc = desc
        return self

    def limit(self, n):
        self._limit_val = n
        return self

    def insert(self, record):
        self._insert_data = record
        return self

    def delete(self):
        self._do_delete = True
        return self

    def execute(self):
        # INSERT
        if self._insert_data is not None:
            data = _local_load(self.table_name)
            record = dict(self._insert_data)
            record["id"] = str(uuid.uuid4())
            record["created_at"] = datetime.now().isoformat()
            data.append(record)
            _local_save(self.table_name, data)
            return Result([record])

        # DELETE
        if self._do_delete:
            data = _local_load(self.table_name)
            for op, col, val in self._filters:
                if op == "eq":
                    data = [r for r in data if str(r.get(col, "")) != str(val)]
            _local_save(self.table_name, data)
            return Result([])

        # SELECT
        data = _local_load(self.table_name)
        for op, col, val in self._filters:
            if op == "eq":
                data = [r for r in data if str(r.get(col, "")) == str(val)]
            elif op == "gte":
                data = [r for r in data if str(r.get(col, "")) >= str(val)]
            elif op == "lte":
                data = [r for r in data if str(r.get(col, "")) <= str(val)]

        if self._order_col:
            data.sort(key=lambda r: r.get(self._order_col, ""), reverse=self._order_desc)

        total = len(data)
        if self._limit_val:
            data = data[:self._limit_val]

        return Result(data, total)


# ============================================
# Unified DB client
# ============================================
class UnifiedDB:
    """Supabase when available, local JSON otherwise — same API."""

    def table(self, name):
        client = _get_supabase_client()
        if client:
            return client.table(name)
        return Query(name)


# ============================================
# Public API
# ============================================
_db = UnifiedDB()


def get_supabase():
    """Return a unified DB client (Supabase-first, local-fallback)."""
    return _db
