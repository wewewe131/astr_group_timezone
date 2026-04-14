import asyncio
from types import SimpleNamespace

from handlers.time_handler import TimeCommandHandler
from services.storage_service import StorageService
from services.time_service import TimeService
from tests.helpers import FakeBot, FakeEvent, FakeRenderService, collect


def test_time_route_unknown_subcommand(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        event = FakeEvent("/time what", group_id="g1")
        result = await collect(handler.handle(event))
        assert len(result) == 1
        assert "未知子命令：what" in result[0]

    asyncio.run(_run())


def test_time_requires_group_for_default_show(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        event = FakeEvent("/time")
        result = await collect(handler.handle(event))
        assert result == ["该指令只能在群组中使用"]

    asyncio.run(_run())


def test_time_set_and_list_routes(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        set_evt = FakeEvent(
            "/time set +8",
            group_id="g1",
            sender_id="u1",
            sender_name="用户名",
            sender_card="当前群名片",
            group_members={"u1": ("当前群名片", "用户名")},
        )
        set_result = await collect(handler.handle(set_evt))
        assert "已登记 当前群名片 的时区为 UTC+08:00" in set_result[0]

        list_evt = FakeEvent(
            "/time list",
            group_id="g1",
            sender_id="u1",
            sender_name="用户名",
            sender_card="当前群名片",
            group_members={"u1": ("当前群名片", "用户名")},
        )
        list_result = await collect(handler.handle(list_evt))
        assert "本群已登记 1 人" in list_result[0]
        assert "当前群名片" in list_result[0]

    asyncio.run(_run())


def test_time_falls_back_to_username_when_card_is_blank(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        set_evt = FakeEvent(
            "/time set +8",
            group_id="g1",
            sender_id="u1",
            sender_name="用户名",
            sender_card="",
            group_members={"u1": ("", "用户名")},
        )
        set_result = await collect(handler.handle(set_evt))
        assert "已登记 用户名 的时区为 UTC+08:00" in set_result[0]

        list_evt = FakeEvent(
            "/time list",
            group_id="g1",
            sender_id="u1",
            sender_name="用户名",
            sender_card="",
            group_members={"u1": ("", "用户名")},
        )
        list_result = await collect(handler.handle(list_evt))
        assert "用户名" in list_result[0]
        assert "· u1" not in list_result[0]

    asyncio.run(_run())


def test_time_list_uses_raw_aiocqhttp_nickname_when_card_is_blank(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        await storage.upsert_timezone("g1", "u1", "Asia/Shanghai")
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        group_obj = SimpleNamespace(
            members=[
                SimpleNamespace(user_id="u1", nickname="AstrBot昵称"),
            ]
        )
        bot = FakeBot(
            members=[
                {"user_id": "u1", "card": "", "nickname": "AstrBot昵称"},
            ]
        )
        event = FakeEvent(
            "/time list",
            group_id="g1",
            sender_id="u1",
            sender_name="AstrBot昵称",
            sender_card="",
            group_obj=group_obj,
            bot=bot,
        )
        result = await collect(handler.handle(event))

        assert "AstrBot昵称" in result[0]
        assert "· u1" not in result[0]

    asyncio.run(_run())


def test_time_list_uses_raw_aiocqhttp_group_cards_when_get_group_only_has_nickname(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        await storage.upsert_timezone("g1", "u1", "Asia/Shanghai")
        await storage.upsert_timezone("g1", "u2", "Europe/London")
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        group_obj = SimpleNamespace(
            members=[
                SimpleNamespace(user_id="u1", nickname="发送者昵称"),
                SimpleNamespace(user_id="u2", nickname="目标昵称"),
            ]
        )
        bot = FakeBot(
            members=[
                {"user_id": "u1", "card": "发送者群名片", "nickname": "发送者昵称"},
                {"user_id": "u2", "card": "目标群名片", "nickname": "目标昵称"},
            ]
        )
        event = FakeEvent(
            "/time list",
            group_id="g1",
            sender_id="u1",
            sender_name="发送者昵称",
            sender_card="发送者群名片",
            group_obj=group_obj,
            bot=bot,
        )
        result = await collect(handler.handle(event))

        assert "发送者群名片" in result[0]
        assert "目标群名片" in result[0]
        assert "发送者昵称" not in result[0]
        assert "目标昵称" not in result[0]

    asyncio.run(_run())


def test_time_list_uses_raw_aiocqhttp_nickname_when_card_is_blank_for_other_member(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        await storage.upsert_timezone("g1", "u2", "Europe/London")
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        bot = FakeBot(
            members=[
                {"user_id": "u2", "card": "", "nickname": "目标昵称"},
            ]
        )
        event = FakeEvent(
            "/time list",
            group_id="g1",
            sender_id="viewer1",
            bot=bot,
        )
        result = await collect(handler.handle(event))

        assert "目标昵称" in result[0]
        assert "· u2" not in result[0]

    asyncio.run(_run())


def test_time_list_prefers_alias_over_group_card(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        await storage.upsert_timezone("g1", "u1", "Asia/Shanghai")
        await storage.set_alias("viewer1", "u1", "老王")
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        event = FakeEvent(
            "/time list",
            group_id="g1",
            sender_id="viewer1",
            group_members={"u1": ("当前群名片", "用户名")},
        )
        result = await collect(handler.handle(event))

        assert "老王" in result[0]
        assert "当前群名片" not in result[0]

    asyncio.run(_run())


def test_time_list_matches_db_users_to_group_member_cards(tmp_path):
    async def _run():
        storage = StorageService(sqlite_db_path=tmp_path / "data_v4.db")
        await storage.initialize()
        await storage.upsert_timezone("g1", "u1", "Asia/Shanghai")
        await storage.upsert_timezone("g1", "u2", "Europe/London")
        handler = TimeCommandHandler(storage, TimeService(), FakeRenderService())

        event = FakeEvent(
            "/time list",
            group_id="g1",
            sender_id="u1",
            sender_name="发送者昵称",
            sender_card="发送者群名片",
            group_members={
                "u1": {"card": "发送者群名片", "nickname": "发送者昵称"},
                "u2": {"card": "目标群名片", "nickname": "目标昵称"},
            },
        )
        result = await collect(handler.handle(event))

        assert "发送者群名片" in result[0]
        assert "目标群名片" in result[0]
        assert "· u2" not in result[0]

    asyncio.run(_run())
