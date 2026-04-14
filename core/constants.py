import re

KV_KEY = "timezones"
ALIAS_KV_KEY = "aliases"
ALIAS_MAX_LEN = 24
QQ_AVATAR_URL = "https://q1.qlogo.cn/g?b=qq&nk={uid}&s=100"
QQ_PLATFORMS = {"aiocqhttp", "qq_official"}
OFFSET_RE = re.compile(
    r"^(?:UTC|GMT)?\s*([+-])?\s*(\d{1,2})(?::?(\d{2}))?$", re.IGNORECASE
)
DIVIDER = "─" * 14

HELP_TEXT = (
    "时间插件用法\n"
    f"{DIVIDER}\n"
    "/time\n"
    "  查看本群所有登记成员的当前时间\n"
    "/time @成员 [@成员...]\n"
    "  仅查看指定成员的当前时间\n"
    "/time set <时区>\n"
    "  登记/修改自己的时区\n"
    "  例：/time set Asia/Shanghai\n"
    "  例：/time set +8\n"
    "  建议使用地区时区以自动处理夏令时（如 /time set America/New_York）\n"
    "/time unset\n"
    "  移除自己的时区登记\n"
    "/time list\n"
    "  列出本群所有登记\n"
    "/time show\n"
    "  输出当前事件的 raw_message 调试信息\n"
    "/time help\n"
    "  显示本帮助\n"
    "/alias @成员 <别名>\n"
    "  为该成员设置仅你自己可见的名片\n"
    f"{DIVIDER}\n"
    "管理员命令\n"
    "/time admin remove <user_id>\n"
    "  移除指定成员的登记\n"
    "/time admin clear\n"
    "  清空本群所有登记"
)

ALIAS_HELP_TEXT = (
    "名片用法（为群友设置仅你自己可见的备注）\n"
    f"{DIVIDER}\n"
    "/alias\n"
    "  查看你已设置的所有名片\n"
    "/alias @成员\n"
    "  查看你为该成员设置的名片\n"
    "/alias @成员 <别名>\n"
    "  为该成员设置/修改名片\n"
    "/alias @成员 unset\n"
    "  清除你对该成员的名片\n"
    "/alias clear\n"
    "  清除你设置的全部名片\n"
    f"（别名最长 {ALIAS_MAX_LEN} 字符；"
    "/time 列表中的他人显示名将使用你自己设置的名片）"
)

MODULE_HELP_TEXT = (
    "时间插件命令总览\n"
    f"{DIVIDER}\n"
    "【查看时间】\n"
    "/time\n"
    "  查看本群登记成员的当前时间\n"
    "/time @成员 [@成员...]\n"
    "  仅查看指定成员的当前时间\n"
    "/time list\n"
    "  列出本群所有登记\n"
    f"{DIVIDER}\n"
    "【时区登记】\n"
    "/time set <时区>\n"
    "  登记/修改自己的时区\n"
    "  例：/time set Asia/Shanghai\n"
    "  例：/time set +8\n"
    "  建议使用地区时区以自动处理夏令时（如 America/New_York）\n"
    "/time unset\n"
    "  移除自己的时区登记\n"
    f"{DIVIDER}\n"
    "【名片】（仅对自己可见的群友备注）\n"
    "/alias\n"
    "  查看你设置的全部名片\n"
    "/alias @成员 <别名>\n"
    f"  为该成员设置名片（≤ {ALIAS_MAX_LEN} 字符）\n"
    "/alias @成员 unset\n"
    "  清除对该成员的名片\n"
    "/alias clear\n"
    "  清除你设置的全部名片\n"
    f"{DIVIDER}\n"
    "【帮助】\n"
    "/help\n"
    "  显示本总览\n"
    "/time help\n"
    "  /time 详细帮助\n"
    "/alias help\n"
    "  /alias 详细帮助\n"
    f"{DIVIDER}\n"
    "【管理员】\n"
    "/time admin remove <user_id>\n"
    "  移除指定成员的登记\n"
    "/time admin clear\n"
    "  清空本群所有登记"
)

TIME_SET_ALIASES = {"set", "reg", "register", "设置", "注册"}
TIME_UNSET_ALIASES = {"unset", "remove", "del", "delete", "移除", "删除"}
TIME_LIST_ALIASES = {"list", "ls", "列表"}
HELP_ALIASES = {"help", "帮助", "?"}
ALIAS_UNSET_ALIASES = {"unset", "remove", "del", "delete", "移除", "删除", "清除"}
ALIAS_CLEAR_ALIASES = {"clear", "清空", "全部清除", "reset"}
ADMIN_REMOVE_ALIASES = {"remove", "rm", "del", "delete"}
