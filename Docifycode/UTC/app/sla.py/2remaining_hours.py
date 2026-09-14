import pytest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
import sys

# --- テスト用ダミークラス・関数定義 ---

# Ticketクラスのダミー
class Ticket:
    def __init__(self, due_at):
        self.due_at = due_at

# utc_now()のダミー（本来はimportされるものだが、テストでpatchする）
def utc_now():
    return datetime.now(timezone.utc)

# --- テスト対象関数のimport ---
# ここでは、remaining_hours, Ticket, utc_nowが同じモジュールにある前提
# もし別モジュールなら、from <module> import remaining_hours, Ticket, utc_now などとする

# --- pytest用テストコード ---

import builtins

from unittest.mock import patch

# TC1: due_atが未来日時、now未指定（None）の場合、残り時間が正の値で返る
def test_remaining_hours_tc1():
    # due_atを未来に設定
    now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    due_at = now + timedelta(hours=5)
    ticket = Ticket(due_at)
    # utc_now()をpatch
    with patch(__name__ + '.utc_now', return_value=now):
        # 残り時間は5.0
        from __main__ import remaining_hours
        assert remaining_hours(ticket) == 5.0

# TC2: due_atが過去日時、now未指定（None）の場合、残り時間が負の値で返る
def test_remaining_hours_tc2():
    now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    due_at = now - timedelta(hours=3)
    ticket = Ticket(due_at)
    with patch(__name__ + '.utc_now', return_value=now):
        from __main__ import remaining_hours
        assert remaining_hours(ticket) == -3.0

# TC3: due_atが現在日時、now未指定（None）の場合、残り時間が0.0で返る
def test_remaining_hours_tc3():
    now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    due_at = now
    ticket = Ticket(due_at)
    with patch(__name__ + '.utc_now', return_value=now):
        from __main__ import remaining_hours
        assert remaining_hours(ticket) == 0.0

# TC4: due_atがNoneの場合、常に0.0が返る
def test_remaining_hours_tc4():
    ticket = Ticket(None)
    from __main__ import remaining_hours
    assert remaining_hours(ticket) == 0.0

# TC5: nowを指定し、due_atがnowより後の場合、正の値が返る
def test_remaining_hours_tc5():
    now = datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
    due_at = now + timedelta(hours=2)
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    assert remaining_hours(ticket, now) == 2.0

# TC6: nowを指定し、due_atがnowより前の場合、負の値が返る
def test_remaining_hours_tc6():
    now = datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
    due_at = now - timedelta(hours=1)
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    assert remaining_hours(ticket, now) == -1.0

# TC7: nowを指定し、due_atとnowが同じ場合、0.0が返る
def test_remaining_hours_tc7():
    now = datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
    due_at = now
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    assert remaining_hours(ticket, now) == 0.0

# TC8: nowとdue_atの差が秒単位の場合、小数点以下2桁で丸められた値が返る
def test_remaining_hours_tc8():
    now = datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
    due_at = now + timedelta(seconds=90)  # 1.5分 = 0.025時間
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    # 90秒 = 0.025時間, round(0.025, 2) = 0.03
    assert remaining_hours(ticket, now) == 0.03

# TC9: nowとdue_atの差がマイクロ秒単位の場合、丸められて0.0になるケース
def test_remaining_hours_tc9():
    now = datetime(2024, 6, 1, 10, 0, 0, 0, tzinfo=timezone.utc)
    due_at = now + timedelta(microseconds=100)  # 100マイクロ秒
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    # 100マイクロ秒 = 100/3600/1_000_000 = 2.777...e-08時間, roundで0.0
    assert remaining_hours(ticket, now) == 0.0

# TC10: nowが不正な型（文字列）の場合、TypeErrorが発生
def test_remaining_hours_tc10():
    now = "2024-06-01T12:00:00"
    due_at = datetime(2024, 6, 1, 13, 0, 0, tzinfo=timezone.utc)
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    with pytest.raises(TypeError):
        remaining_hours(ticket, now)

# TC11: due_atが不正な型（文字列）の場合、TypeErrorが発生
def test_remaining_hours_tc11():
    due_at = "2024-06-01T13:00:00"
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    with pytest.raises(TypeError):
        remaining_hours(ticket)

# TC12: due_atとnowのタイムゾーンが異なる場合、差分が正しく計算されるか
def test_remaining_hours_tc12():
    # due_at: UTC, now: JST
    due_at = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    now = datetime(2024, 6, 1, 21, 0, 0, tzinfo=timezone(timedelta(hours=9)))  # JST
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    # JST 21:00 == UTC 12:00, 差は0
    assert remaining_hours(ticket, now) == 0.0

# TC13: ticketにdue_at属性が存在しない場合、AttributeErrorが発生
def test_remaining_hours_tc13():
    class NoDueAt:
        pass
    ticket = NoDueAt()
    from __main__ import remaining_hours
    with pytest.raises(AttributeError):
        remaining_hours(ticket)

# TC14: utc_now()がdatetime型以外を返した場合、TypeErrorが発生
def test_remaining_hours_tc14():
    due_at = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    ticket = Ticket(due_at)
    # utc_now()がstrを返すようにpatch
    with patch(__name__ + '.utc_now', return_value="not a datetime"):
        from __main__ import remaining_hours
        with pytest.raises(TypeError):
            remaining_hours(ticket)

# TC15: due_atとnowがUNIX epoch（1970-01-01 00:00:00）で同じ場合、0.0が返る
def test_remaining_hours_tc15():
    now = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    due_at = now
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    assert remaining_hours(ticket, now) == 0.0

# TC16: due_atがdatetime型の最大値の場合、残り時間が非常に大きい正の値で返る
def test_remaining_hours_tc16():
    now = datetime.now(timezone.utc)
    due_at = datetime.max.replace(tzinfo=timezone.utc)
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    result = remaining_hours(ticket, now)
    # 非常に大きい正の値
    assert result > 1e6

# TC17: due_atがdatetime型の最小値の場合、残り時間が非常に大きい負の値で返る
def test_remaining_hours_tc17():
    now = datetime.now(timezone.utc)
    due_at = datetime.min.replace(tzinfo=timezone.utc)
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    result = remaining_hours(ticket, now)
    # 非常に大きい負の値
    assert result < -1e6

# TC18: due_atとnowが1時間未満（30分）の差の場合、0.5が返る
def test_remaining_hours_tc18():
    now = datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
    due_at = now + timedelta(minutes=30)
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    assert remaining_hours(ticket, now) == 0.5

# TC19: due_atとnowが1秒未満の差の場合、丸めて0.0が返る
def test_remaining_hours_tc19():
    now = datetime(2024, 6, 1, 10, 0, 0, 0, tzinfo=timezone.utc)
    due_at = now + timedelta(milliseconds=500)  # 0.5秒
    ticket = Ticket(due_at)
    from __main__ import remaining_hours
    # 0.5秒 = 0.000138...時間, roundで0.0
    assert remaining_hours(ticket, now) == 0.0

# TC20: now未指定時、utc_now()の返す現在時刻との差分が返る
def test_remaining_hours_tc20():
    now = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    due_at = now + timedelta(hours=1)
    ticket = Ticket(due_at)
    with patch(__name__ + '.utc_now', return_value=now):
        from __main__ import remaining_hours
        assert remaining_hours(ticket) == 1.0
```
