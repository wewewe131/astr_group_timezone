import asyncio

from core.constants import ALIAS_KV_KEY, KV_KEY
from services.storage_service import StorageService


def test_initialize_migrates_aliases_and_drops_legacy():
    async def _run():
        async def fake_get(key, default):
            if key == KV_KEY:
                return {"g1": {"u1": {"tz": "UTC+08:00", "name": "A"}}}
            if key == ALIAS_KV_KEY:
                return {
                    "owner1": {"u2": "老王", "u3": ""},
                    "owner2": "legacy-global-alias",
                }
            return default

        async def fake_put(key, value):
            return None

        svc = StorageService(fake_get, fake_put)
        await svc.initialize()

        assert "g1" in svc.data
        assert svc.aliases == {"owner1": {"u2": "老王"}}

    asyncio.run(_run())
