"""测试 greeter 模块。"""
import pytest
from src.greeter import get_greeting, format_greeting


def test_morning_greeting():
    # TC-GREETER-001: 早上时段
    assert get_greeting(8) == "早上好"


def test_afternoon_greeting():
    # TC-GREETER-002: 下午时段
    assert get_greeting(14) == "下午好"


def test_night_greeting():
    # TC-GREETER-003: 深夜时段
    assert get_greeting(23) == "你好"


def test_formal_greeting():
    # TC-GREETER-004: 正式问候
    result = format_greeting("Alice", "早上好", formal=True)
    assert result == "尊敬的 Alice，早上好！"


def test_edge_morning_start():
    assert get_greeting(6) == "早上好"


def test_edge_morning_end():
    assert get_greeting(11) == "早上好"


def test_edge_afternoon_start():
    assert get_greeting(12) == "下午好"


def test_edge_evening():
    assert get_greeting(18) == "晚上好"


def test_edge_evening_end():
    assert get_greeting(21) == "晚上好"


def test_edge_dawn():
    assert get_greeting(5) == "你好"
