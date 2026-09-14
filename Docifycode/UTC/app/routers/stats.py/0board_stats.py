import pytest

# BoardStatsOut, StatsService, get_stats_service, board_stats をインポート
from somewhere import BoardStatsOut, StatsService, get_stats_service, board_stats

# FastAPIのDependsをモックするため
from fastapi import Depends

# --- テスト用モッククラスとヘルパー ---

class MockStatsServiceNormal:
    # TC2, TC5, TC9用: summarize()が正常な値や空値を返す
    def __init__(self, result):
        self._result = result
    def summarize(self):
        return self._result

class MockStatsServiceException:
    # TC3用: summarize()が例外を投げる
    def summarize(self):
        raise Exception("summarize error")

class MockStatsServiceNone:
    # TC4, TC10用: summarize()がNoneを返す
    def summarize(self):
        return None

class MockStatsServiceInvalidType:
    # TC6, TC8用: summarize()が不正な型を返す
    def __init__(self, result):
        self._result = result
    def summarize(self):
        return self._result

# --- テストケース ---

# TC1: StatsServiceインスタンス # 正常なStatsServiceオブジェクト
def test_board_stats_TC1():
    # 正常なStatsServiceインスタンスを使う
    service = StatsService()
    # BoardStatsOut型の戻り値を期待
    result = board_stats(service)
    # BoardStatsOut型であることを確認
    assert isinstance(result, BoardStatsOut)

# TC2: StatsServiceのモック # summarize()が正常な値を返すモック
def test_board_stats_TC2():
    # summarize()が正常なBoardStatsOutを返すモック
    expected = BoardStatsOut()
    service = MockStatsServiceNormal(expected)
    result = board_stats(service)
    assert result == expected

# TC3: StatsServiceのモック # summarize()が例外を投げるモック
def test_board_stats_TC3():
    service = MockStatsServiceException()
    # 例外が投げられることを期待
    with pytest.raises(Exception):
        board_stats(service)

# TC4: StatsServiceのモック # summarize()がNoneを返すモック
def test_board_stats_TC4():
    service = MockStatsServiceNone()
    # TypeErrorが発生することを期待
    with pytest.raises(TypeError):
        board_stats(service)

# TC5: StatsServiceのモック # summarize()が空のBoardStatsOutを返すモック
def test_board_stats_TC5():
    # 空のBoardStatsOut（全フィールド初期値）を返すモック
    empty = BoardStatsOut()
    service = MockStatsServiceNormal(empty)
    result = board_stats(service)
    assert result == empty

# TC6: StatsServiceのモック # summarize()が不正な型を返すモック
def test_board_stats_TC6():
    # summarize()がdict型を返すモック
    service = MockStatsServiceInvalidType({"foo": "bar"})
    with pytest.raises(TypeError):
        board_stats(service)

# TC7: null # serviceがNoneの場合
def test_board_stats_TC7():
    # serviceがNoneの場合
    with pytest.raises(TypeError):
        board_stats(None)

# TC8: StatsServiceのモック # summarize()がint型を返すモック
def test_board_stats_TC8():
    service = MockStatsServiceInvalidType(123)
    with pytest.raises(TypeError):
        board_stats(service)

# TC9: StatsServiceのモック # summarize()が空のBoardStatsOutを返すモック（境界値）
def test_board_stats_TC9():
    empty = BoardStatsOut()
    service = MockStatsServiceNormal(empty)
    result = board_stats(service)
    assert result == empty

# TC10: StatsServiceのモック # summarize()がNoneを返すモック（空値返却）
def test_board_stats_TC10():
    service = MockStatsServiceNone()
    with pytest.raises(TypeError):
        board_stats(service)
```
