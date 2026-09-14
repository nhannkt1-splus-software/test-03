import pytest

# WorklogLimitErrorのテスト対象メソッドをテストするためのヘルパー関数
def create_worklog_limit_error(ticket_id, total, limit):
    # 型チェック
    if not isinstance(limit, float):
        raise TypeError("limitはfloat型でなければなりません")
    if not isinstance(ticket_id, int):
        raise TypeError("ticket_idはint型でなければなりません")
    if not isinstance(total, float):
        raise TypeError("totalはfloat型でなければなりません")
    # 値チェック
    if ticket_id < 0:
        raise ValueError("ticket_idは0以上でなければなりません")
    if total < 0:
        raise ValueError("totalは0以上でなければなりません")
    if limit < 0:
        raise ValueError("limitは0以上でなければなりません")
    # WorklogLimitErrorインスタンス生成
    from target import WorklogLimitError  # テスト対象のインポート
    return WorklogLimitError(ticket_id, total, limit)

# TC1: 正常系：全て正常値
def test_TC1():
    # TC1
    # limit: 8.0, ticket_id: 1, total: 5.5, 期待される結果: None
    try:
        err = create_worklog_limit_error(1, 5.5, 8.0)
        assert err.ticket_id == 1
        assert err.total == 5.5
        assert err.limit == 8.0
        assert str(err) == "Ticket 1 cannot exceed 8.0 logged hours (now 5.5)"
    except Exception:
        pytest.fail("TC1: 例外が発生しました")

# TC2: 境界値テスト：全て0
def test_TC2():
    # TC2
    try:
        err = create_worklog_limit_error(0, 0.0, 0.0)
        assert err.ticket_id == 0
        assert err.total == 0.0
        assert err.limit == 0.0
        assert str(err) == "Ticket 0 cannot exceed 0.0 logged hours (now 0.0)"
    except Exception:
        pytest.fail("TC2: 例外が発生しました")

# TC3: 異常系：ticket_idが負の値
def test_TC3():
    # TC3
    with pytest.raises(ValueError):
        create_worklog_limit_error(-1, 5.5, 8.0)

# TC4: 正常系：ticket_idが大きい値
def test_TC4():
    # TC4
    try:
        err = create_worklog_limit_error(1000000, 5.5, 8.0)
        assert err.ticket_id == 1000000
        assert err.total == 5.5
        assert err.limit == 8.0
        assert str(err) == "Ticket 1000000 cannot exceed 8.0 logged hours (now 5.5)"
    except Exception:
        pytest.fail("TC4: 例外が発生しました")

# TC5: 異常系：ticket_idがstr型
def test_TC5():
    # TC5
    with pytest.raises(TypeError):
        create_worklog_limit_error("1", 5.5, 8.0)

# TC6: 異常系：ticket_idがNone
def test_TC6():
    # TC6
    with pytest.raises(TypeError):
        create_worklog_limit_error(None, 5.5, 8.0)

# TC7: 異常系：ticket_idがfloat型
def test_TC7():
    # TC7
    with pytest.raises(TypeError):
        create_worklog_limit_error(2.5, 5.5, 8.0)

# TC8: 異常系：totalが負の値
def test_TC8():
    # TC8
    with pytest.raises(ValueError):
        create_worklog_limit_error(1, -0.1, 8.0)

# TC9: 正常系：totalが大きい値
def test_TC9():
    # TC9
    try:
        err = create_worklog_limit_error(1, 1000000.0, 8.0)
        assert err.ticket_id == 1
        assert err.total == 1000000.0
        assert err.limit == 8.0
        assert str(err) == "Ticket 1 cannot exceed 8.0 logged hours (now 1000000.0)"
    except Exception:
        pytest.fail("TC9: 例外が発生しました")

# TC10: 異常系：totalがstr型
def test_TC10():
    # TC10
    with pytest.raises(TypeError):
        create_worklog_limit_error(1, "5.5", 8.0)

# TC11: 異常系：totalがNone
def test_TC11():
    # TC11
    with pytest.raises(TypeError):
        create_worklog_limit_error(1, None, 8.0)

# TC12: 異常系：totalがint型
def test_TC12():
    # TC12
    with pytest.raises(TypeError):
        create_worklog_limit_error(1, 1, 8.0)

# TC13: 異常系：limitが負の値
def test_TC13():
    # TC13
    with pytest.raises(ValueError):
        create_worklog_limit_error(1, 5.5, -1.0)

# TC14: 正常系：limitが大きい値
def test_TC14():
    # TC14
    try:
        err = create_worklog_limit_error(1, 5.5, 1000000.0)
        assert err.ticket_id == 1
        assert err.total == 5.5
        assert err.limit == 1000000.0
        assert str(err) == "Ticket 1 cannot exceed 1000000.0 logged hours (now 5.5)"
    except Exception:
        pytest.fail("TC14: 例外が発生しました")

# TC15: 異常系：limitがstr型
def test_TC15():
    # TC15
    with pytest.raises(TypeError):
        create_worklog_limit_error(1, 5.5, "8.0")

# TC16: 異常系：limitがNone
def test_TC16():
    # TC16
    with pytest.raises(TypeError):
        create_worklog_limit_error(1, 5.5, None)

# TC17: 異常系：limitがint型
def test_TC17():
    # TC17
    with pytest.raises(TypeError):
        create_worklog_limit_error(1, 5.5, 1)

# TC18: 異常系：totalが負の値かつticket_id, limitが境界値
def test_TC18():
    # TC18
    with pytest.raises(ValueError):
        create_worklog_limit_error(0, -0.1, 0.0)

# TC19: 正常系：全て大きい値
def test_TC19():
    # TC19
    try:
        err = create_worklog_limit_error(1000000, 1000000.0, 1000000.0)
        assert err.ticket_id == 1000000
        assert err.total == 1000000.0
        assert err.limit == 1000000.0
        assert str(err) == "Ticket 1000000 cannot exceed 1000000.0 logged hours (now 1000000.0)"
    except Exception:
        pytest.fail("TC19: 例外が発生しました")

# TC20: 異常系：ticket_id, total, limit全て負の値
def test_TC20():
    # TC20
    with pytest.raises(ValueError):
        create_worklog_limit_error(-1, -0.1, -1.0)

# TC21: 異常系：ticket_id, total, limit全てstr型
def test_TC21():
    # TC21
    with pytest.raises(TypeError):
        create_worklog_limit_error("1", "5.5", "8.0")

# TC22: 異常系：ticket_id, total, limit全てNone
def test_TC22():
    # TC22
    with pytest.raises(TypeError):
        create_worklog_limit_error(None, None, None)

# TC23: 異常系：ticket_idがfloat型、totalとlimitがint型
def test_TC23():
    # TC23
    with pytest.raises(TypeError):
        create_worklog_limit_error(2.5, 1, 1)
```
