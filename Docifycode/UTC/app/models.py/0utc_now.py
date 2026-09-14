import pytest
from datetime import datetime, timezone
import time

# テスト対象関数をインポート
from target_module import utc_now  # 必要に応じてモジュール名を修正してください

# TC1: 正常系：引数なしで現在のUTC時刻がdatetime型（tzinfoがtimezone.utc）で返されることを確認
def test_utc_now_returns_datetime_with_utc_tzinfo():  # TC1
    result = utc_now()
    # datetime型であること
    assert isinstance(result, datetime)
    # tzinfoがtimezone.utcであること
    assert result.tzinfo == timezone.utc

# TC2: 正常系：返却値のtzinfoが必ずtimezone.utcであることを確認するテスト
def test_utc_now_tzinfo_is_timezone_utc():  # TC2
    result = utc_now()
    # tzinfoがtimezone.utcであること
    assert result.tzinfo == timezone.utc

# TC3: 正常系：連続で呼び出した場合に返却値が異なる（時刻が進んでいる）ことを確認するテスト
def test_utc_now_returns_different_values_on_subsequent_calls():  # TC3
    result1 = utc_now()
    time.sleep(0.01)  # 10ミリ秒待機
    result2 = utc_now()
    # 2回の呼び出しで値が異なること（時刻が進んでいること）
    assert result2 > result1

# TC4: 正常系：返却値が必ずdatetime型であることを確認するテスト
def test_utc_now_returns_datetime_instance():  # TC4
    result = utc_now()
    assert isinstance(result, datetime)

# TC5: 正常系：返却値の年・月・日・時・分・秒が有効な範囲（例えば月は1～12、日付は1～31など）であることを確認するテスト
def test_utc_now_datetime_fields_are_in_valid_range():  # TC5
    result = utc_now()
    # 年は1以上
    assert result.year >= 1
    # 月は1～12
    assert 1 <= result.month <= 12
    # 日は1～31
    assert 1 <= result.day <= 31
    # 時は0～23
    assert 0 <= result.hour <= 23
    # 分は0～59
    assert 0 <= result.minute <= 59
    # 秒は0～59
    assert 0 <= result.second <= 59
    # マイクロ秒は0～999999
    assert 0 <= result.microsecond <= 999999
```
