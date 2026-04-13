import pytest

from services.time_service import TimeService


def test_parse_tz_region_success():
    svc = TimeService()
    _, canonical = svc.parse_tz("Asia/Shanghai")
    assert canonical == "Asia/Shanghai"


def test_parse_tz_offset_success():
    svc = TimeService()
    _, canonical = svc.parse_tz("+8")
    assert canonical == "UTC+08:00"


def test_parse_tz_offset_with_minutes_success():
    svc = TimeService()
    _, canonical = svc.parse_tz("UTC-05:30")
    assert canonical == "UTC-05:30"


@pytest.mark.parametrize("raw", ["+15", "+8:99", "bad/tz"])
def test_parse_tz_invalid(raw):
    svc = TimeService()
    with pytest.raises(ValueError):
        svc.parse_tz(raw)
