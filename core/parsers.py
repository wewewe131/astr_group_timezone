from __future__ import annotations

from typing import Any


def strip_cmd_prefix(raw: str, names: tuple[str, ...] = ("time",)) -> list[str]:
    tokens = (raw or "").strip().split()
    for i, tok in enumerate(tokens):
        if tok.lstrip("/!").lower() in names:
            return tokens[i + 1 :]
    return tokens


def _message_chain(event: Any) -> list[Any]:
    try:
        return list(event.get_messages() or [])
    except Exception:
        return []


def _is_at_component(comp: Any) -> bool:
    return comp.__class__.__name__ == "At" or hasattr(comp, "qq")


def extract_mentions_and_text(event: Any) -> tuple[list[str], str]:
    """一次遍历同时提取 @ 目标和去 mention 后的纯文本。"""
    self_id = ""
    try:
        self_id = str(getattr(event.message_obj, "self_id", "") or "")
    except Exception:
        pass

    targets: list[str] = []
    parts: list[str] = []
    for comp in _message_chain(event):
        if _is_at_component(comp):
            qq = str(getattr(comp, "qq", "") or "").strip()
            if qq and qq.lower() != "all" and (not self_id or qq != self_id) and qq not in targets:
                targets.append(qq)
            parts.append(" ")
            continue
        text = getattr(comp, "text", None)
        if text is not None:
            parts.append(str(text))
    return targets, "".join(parts).strip()


def extract_at_targets(event: Any) -> list[str]:
    """提取被 @ 的成员 ID（排除机器人自己与 @all）。"""
    targets, _ = extract_mentions_and_text(event)
    return targets


def drop_at_tokens(tokens: list[str]) -> list[str]:
    return [t for t in tokens if not t.startswith("@")]


def extract_text_without_mentions(event: Any) -> str:
    """从消息链中提取非 @ 的纯文本内容。"""
    _, text = extract_mentions_and_text(event)
    return text
