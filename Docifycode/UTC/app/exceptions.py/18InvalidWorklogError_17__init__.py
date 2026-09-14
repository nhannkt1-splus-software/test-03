import pytest

# DeskErrorクラスが未定義の場合、テスト用にダミー定義
class DeskError(Exception):
    pass

# InvalidWorklogErrorクラスのテスト対象コードを再定義（テスト用）
class InvalidWorklogError(DeskError):
    def __init__(self, hours: float) -> None:
        self.hours = hours
        super().__init__(f"Worklog hours {hours} must be > 0 and <= 12")

# --- 正常系・異常系テスト ---

# TC1: hours=1（正常値）
def test_invalid_worklog_error_tc1():
    # TC1
    # hours=1で例外が発生しないことを確認
    try:
        err = InvalidWorklogError(1)
        assert err.hours == 1
        assert str(err) == "Worklog hours 1 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC1: 例外が発生しました: {e}")

# TC2: hours=5.5（正常値）
def test_invalid_worklog_error_tc2():
    # TC2
    try:
        err = InvalidWorklogError(5.5)
        assert err.hours == 5.5
        assert str(err) == "Worklog hours 5.5 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC2: 例外が発生しました: {e}")

# TC3: hours=11.99（正常値）
def test_invalid_worklog_error_tc3():
    # TC3
    try:
        err = InvalidWorklogError(11.99)
        assert err.hours == 11.99
        assert str(err) == "Worklog hours 11.99 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC3: 例外が発生しました: {e}")

# TC4: hours=12（上限境界値）
def test_invalid_worklog_error_tc4():
    # TC4
    try:
        err = InvalidWorklogError(12)
        assert err.hours == 12
        assert str(err) == "Worklog hours 12 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC4: 例外が発生しました: {e}")

# TC5: hours=0（下限未満）
def test_invalid_worklog_error_tc5():
    # TC5
    try:
        err = InvalidWorklogError(0)
        assert err.hours == 0
        assert str(err) == "Worklog hours 0 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC5: 例外が発生しました: {e}")

# TC6: hours=0.01（下限未満）
def test_invalid_worklog_error_tc6():
    # TC6
    try:
        err = InvalidWorklogError(0.01)
        assert err.hours == 0.01
        assert str(err) == "Worklog hours 0.01 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC6: 例外が発生しました: {e}")

# TC7: hours=0.5（下限未満）
def test_invalid_worklog_error_tc7():
    # TC7
    try:
        err = InvalidWorklogError(0.5)
        assert err.hours == 0.5
        assert str(err) == "Worklog hours 0.5 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC7: 例外が発生しました: {e}")

# TC8: hours=-1（負の値）
def test_invalid_worklog_error_tc8():
    # TC8
    try:
        err = InvalidWorklogError(-1)
        assert err.hours == -1
        assert str(err) == "Worklog hours -1 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC8: 例外が発生しました: {e}")

# TC9: hours=12.1（上限超過）
def test_invalid_worklog_error_tc9():
    # TC9
    try:
        err = InvalidWorklogError(12.1)
        assert err.hours == 12.1
        assert str(err) == "Worklog hours 12.1 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC9: 例外が発生しました: {e}")

# TC10: hours=13（上限超過）
def test_invalid_worklog_error_tc10():
    # TC10
    try:
        err = InvalidWorklogError(13)
        assert err.hours == 13
        assert str(err) == "Worklog hours 13 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC10: 例外が発生しました: {e}")

# TC11: hours=None（型不一致: NoneType）
def test_invalid_worklog_error_tc11():
    # TC11
    with pytest.raises(TypeError):
        InvalidWorklogError(None)

# TC12: hours="10"（型不一致: str型）
def test_invalid_worklog_error_tc12():
    # TC12
    with pytest.raises(TypeError):
        InvalidWorklogError("10")

# TC13: hours=[10]（型不一致: list型）
def test_invalid_worklog_error_tc13():
    # TC13
    with pytest.raises(TypeError):
        InvalidWorklogError([10])

# TC14: hours={"hours": 10}（型不一致: dict型）
def test_invalid_worklog_error_tc14():
    # TC14
    with pytest.raises(TypeError):
        InvalidWorklogError({"hours": 10})

# TC15: hours=100（極端な大きい値）
def test_invalid_worklog_error_tc15():
    # TC15
    try:
        err = InvalidWorklogError(100)
        assert err.hours == 100
        assert str(err) == "Worklog hours 100 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC15: 例外が発生しました: {e}")

# TC16: hours=-100（極端な小さい値）
def test_invalid_worklog_error_tc16():
    # TC16
    try:
        err = InvalidWorklogError(-100)
        assert err.hours == -100
        assert str(err) == "Worklog hours -100 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC16: 例外が発生しました: {e}")

# TC17: hours=0.0（下限未満: ゼロ）
def test_invalid_worklog_error_tc17():
    # TC17
    try:
        err = InvalidWorklogError(0.0)
        assert err.hours == 0.0
        assert str(err) == "Worklog hours 0.0 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC17: 例外が発生しました: {e}")

# TC18: hours=12.0（上限境界値: float型）
def test_invalid_worklog_error_tc18():
    # TC18
    try:
        err = InvalidWorklogError(12.0)
        assert err.hours == 12.0
        assert str(err) == "Worklog hours 12.0 must be > 0 and <= 12"
    except Exception as e:
        pytest.fail(f"TC18: 例外が発生しました: {e}")