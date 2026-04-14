import asyncio
import sqlite3

from services.storage_service import ALIASES_TABLE, TIMEZONES_TABLE, StorageService


def test_storage_initializes_tables(tmp_path):
    async def _run():
        svc = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await svc.initialize()

        with sqlite3.connect(tmp_path / "data_v4.db") as conn:
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                ).fetchall()
            }
            timezone_columns = [
                row[1]
                for row in conn.execute(
                    f"PRAGMA table_info({TIMEZONES_TABLE})"
                ).fetchall()
            ]

        assert TIMEZONES_TABLE in tables
        assert ALIASES_TABLE in tables
        assert timezone_columns == ["group_id", "user_id", "tz"]

    asyncio.run(_run())


def test_timezone_query_can_join_alias(tmp_path):
    async def _run():
        svc = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await svc.initialize()
        await svc.upsert_timezone("g1", "u1", "Asia/Shanghai")
        await svc.set_alias("viewer1", "u1", "老王")

        users = await svc.list_timezones("g1", viewer="viewer1")

        assert users == {"u1": {"tz": "Asia/Shanghai", "alias": "老王"}}

    asyncio.run(_run())


def test_storage_crud_methods(tmp_path):
    async def _run():
        svc = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await svc.initialize()

        await svc.upsert_timezone("g1", "u1", "UTC+08:00")
        await svc.upsert_timezone("g1", "u2", "Europe/London")
        await svc.set_alias("viewer1", "u1", "A")
        await svc.set_alias("viewer1", "u2", "B")

        assert await svc.get_timezone("g1", "u1", viewer="viewer1") == {
            "tz": "UTC+08:00",
            "alias": "A",
        }
        assert await svc.list_aliases("viewer1", ["u2"]) == {"u2": "B"}
        assert await svc.delete_aliases("viewer1", ["u1", "u3"]) == {"u1": "A"}
        assert await svc.delete_timezone("g1", "u2") == {"tz": "Europe/London"}
        assert await svc.clear_aliases("viewer1") == 1
        assert await svc.clear_group_timezones("g1") == 1

    asyncio.run(_run())
