import pytest

# DeskErrorが未定義の場合のため、テスト用に定義
class DeskError(Exception):
    pass

# テスト対象クラスのインポートまたは定義
from types import SimpleNamespace

# TicketClosedErrorが既にimportされている前提
# もしimportできない場合は、上記のクラス定義をここに貼り付けてください

# --- 正常系・異常系テスト ---

# TC1: 正常系：ticket_idが正の整数、actionが有効な文字列
def test_TC1():
    # TC1
    err = TicketClosedError(1, "close")
    # ticket_id, action, メッセージの検証
    assert err.ticket_id == 1  # チケットIDが正しくセットされていること
    assert err.action == "close"  # actionが正しくセットされていること
    assert str(err) == "Cannot close closed ticket 1"  # メッセージが正しいこと

# TC2: 境界値テスト：ticket_idが0、actionが有効な文字列
def test_TC2():
    # TC2
    err = TicketClosedError(0, "reopen")
    assert err.ticket_id == 0
    assert err.action == "reopen"
    assert str(err) == "Cannot reopen closed ticket 0"

# TC3: 境界値テスト：ticket_idが負の整数、actionが有効な文字列
def test_TC3():
    # TC3
    err = TicketClosedError(-1, "close")
    assert err.ticket_id == -1
    assert err.action == "close"
    assert str(err) == "Cannot close closed ticket -1"

# TC4: ticket_idが非常に大きい値、actionが有効な文字列
def test_TC4():
    # TC4
    err = TicketClosedError(999999999, "close")
    assert err.ticket_id == 999999999
    assert err.action == "close"
    assert str(err) == "Cannot close closed ticket 999999999"

# TC5: actionが空文字列の場合
def test_TC5():
    # TC5
    err = TicketClosedError(1, "")
    assert err.ticket_id == 1
    assert err.action == ""
    assert str(err) == "Cannot  closed ticket 1"

# TC6: actionが日本語文字列の場合
def test_TC6():
    # TC6
    err = TicketClosedError(1, "削除")
    assert err.ticket_id == 1
    assert err.action == "削除"
    assert str(err) == "Cannot 削除 closed ticket 1"

# TC7: ticket_idがNoneの場合（型違いエラー）
def test_TC7():
    # TC7
    with pytest.raises(TypeError):
        TicketClosedError(None, "close")

# TC8: actionがNoneの場合（型違いエラー）
def test_TC8():
    # TC8
    with pytest.raises(TypeError):
        TicketClosedError(1, None)

# TC9: ticket_idがstr型の場合（型違いエラー）
def test_TC9():
    # TC9
    with pytest.raises(TypeError):
        TicketClosedError("1", "close")

# TC10: ticket_idがfloat型の場合（型違いエラー）
def test_TC10():
    # TC10
    with pytest.raises(TypeError):
        TicketClosedError(1.5, "close")

# TC11: ticket_idがlist型の場合（型違いエラー）
def test_TC11():
    # TC11
    with pytest.raises(TypeError):
        TicketClosedError([1], "close")

# TC12: ticket_idがdict型の場合（型違いエラー）
def test_TC12():
    # TC12
    with pytest.raises(TypeError):
        TicketClosedError({}, "close")

# TC13: ticket_idがbool型の場合（Pythonではboolはintのサブクラスなので正常系）
def test_TC13():
    # TC13
    err = TicketClosedError(True, "close")
    assert err.ticket_id is True
    assert err.action == "close"
    assert str(err) == "Cannot close closed ticket True"

# TC14: ticket_idがbool型の場合（Pythonではboolはintのサブクラスなので正常系）
def test_TC14():
    # TC14
    err = TicketClosedError(False, "close")
    assert err.ticket_id is False
    assert err.action == "close"
    assert str(err) == "Cannot close closed ticket False"

# TC15: actionがint型の場合（型違いエラー）
def test_TC15():
    # TC15
    with pytest.raises(TypeError):
        TicketClosedError(1, 123)

# TC16: actionがfloat型の場合（型違いエラー）
def test_TC16():
    # TC16
    with pytest.raises(TypeError):
        TicketClosedError(1, 1.5)

# TC17: actionがlist型の場合（型違いエラー）
def test_TC17():
    # TC17
    with pytest.raises(TypeError):
        TicketClosedError(1, ["close"])

# TC18: actionがdict型の場合（型違いエラー）
def test_TC18():
    # TC18
    with pytest.raises(TypeError):
        TicketClosedError(1, {})

# TC19: ticket_idが非常に大きい値、actionが有効な文字列（組み合わせパターン）
def test_TC19():
    # TC19
    err = TicketClosedError(999999999, "reopen")
    assert err.ticket_id == 999999999
    assert err.action == "reopen"
    assert str(err) == "Cannot reopen closed ticket 999999999"

# TC20: ticket_idが負の整数、actionが有効な文字列（組み合わせパターン）
def test_TC20():
    # TC20
    err = TicketClosedError(-1, "reopen")
    assert err.ticket_id == -1
    assert err.action == "reopen"
    assert str(err) == "Cannot reopen closed ticket -1"

# TC21: ticket_idが0、actionが空文字列（組み合わせパターン）
def test_TC21():
    # TC21
    err = TicketClosedError(0, "")
    assert err.ticket_id == 0
    assert err.action == ""
    assert str(err) == "Cannot  closed ticket 0"

# TC22: ticket_idがbool型、actionが空文字列（組み合わせパターン）
def test_TC22():
    # TC22
    err = TicketClosedError(True, "")
    assert err.ticket_id is True
    assert err.action == ""
    assert str(err) == "Cannot  closed ticket True"

# TC23: ticket_idがbool型、actionが日本語文字列（組み合わせパターン）
def test_TC23():
    # TC23
    err = TicketClosedError(False, "削除")
    assert err.ticket_id is False
    assert err.action == "削除"
    assert str(err) == "Cannot 削除 closed ticket False"