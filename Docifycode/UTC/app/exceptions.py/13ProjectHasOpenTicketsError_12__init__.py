import pytest

# DeskErrorのダミークラスを定義（テスト用）
class DeskError(Exception):
    pass

# テスト対象クラスのインポートまたは再定義
class ProjectHasOpenTicketsError(DeskError):
    def __init__(self, project_id: int, count: int) -> None:
        self.project_id = project_id
        self.count = count
        super().__init__(f"Cannot archive project {project_id}: {count} open ticket(s)")

# --- 正常系テスト ---

# TC1: project_idとcountが正の整数
def test_TC1():
    # TC1
    err = ProjectHasOpenTicketsError(1, 5)
    assert err.project_id == 1  # project_idが正しくセットされているか
    assert err.count == 5       # countが正しくセットされているか
    assert str(err) == "Cannot archive project 1: 5 open ticket(s)"

# TC2: project_idが0（境界値）
def test_TC2():
    # TC2
    err = ProjectHasOpenTicketsError(0, 5)
    assert err.project_id == 0
    assert err.count == 5
    assert str(err) == "Cannot archive project 0: 5 open ticket(s)"

# TC3: project_idが負の整数
def test_TC3():
    # TC3
    err = ProjectHasOpenTicketsError(-1, 5)
    assert err.project_id == -1
    assert err.count == 5
    assert str(err) == "Cannot archive project -1: 5 open ticket(s)"

# TC4: project_idが非常に大きい整数
def test_TC4():
    # TC4
    err = ProjectHasOpenTicketsError(999999999, 5)
    assert err.project_id == 999999999
    assert err.count == 5
    assert str(err) == "Cannot archive project 999999999: 5 open ticket(s)"

# TC5: countが0（境界値）
def test_TC5():
    # TC5
    err = ProjectHasOpenTicketsError(1, 0)
    assert err.project_id == 1
    assert err.count == 0
    assert str(err) == "Cannot archive project 1: 0 open ticket(s)"

# TC6: countが負の整数
def test_TC6():
    # TC6
    err = ProjectHasOpenTicketsError(1, -1)
    assert err.project_id == 1
    assert err.count == -1
    assert str(err) == "Cannot archive project 1: -1 open ticket(s)"

# TC7: countが非常に大きい整数
def test_TC7():
    # TC7
    err = ProjectHasOpenTicketsError(1, 999999999)
    assert err.project_id == 1
    assert err.count == 999999999
    assert str(err) == "Cannot archive project 1: 999999999 open ticket(s)"

# TC14: project_idとcountが両方非常に大きい整数
def test_TC14():
    # TC14
    err = ProjectHasOpenTicketsError(999999999, 999999999)
    assert err.project_id == 999999999
    assert err.count == 999999999
    assert str(err) == "Cannot archive project 999999999: 999999999 open ticket(s)"

# TC15: project_idとcountが両方負の整数
def test_TC15():
    # TC15
    err = ProjectHasOpenTicketsError(-1, -1)
    assert err.project_id == -1
    assert err.count == -1
    assert str(err) == "Cannot archive project -1: -1 open ticket(s)"

# TC16: project_idとcountが両方ゼロ
def test_TC16():
    # TC16
    err = ProjectHasOpenTicketsError(0, 0)
    assert err.project_id == 0
    assert err.count == 0
    assert str(err) == "Cannot archive project 0: 0 open ticket(s)"

# --- 異常系テスト ---

# TC8: project_idがstr型（型不一致）
def test_TC8():
    # TC8
    with pytest.raises(TypeError):
        ProjectHasOpenTicketsError("1", 5)

# TC9: project_idがNone（型不一致）
def test_TC9():
    # TC9
    with pytest.raises(TypeError):
        ProjectHasOpenTicketsError(None, 5)

# TC10: countがstr型（型不一致）
def test_TC10():
    # TC10
    with pytest.raises(TypeError):
        ProjectHasOpenTicketsError(1, "5")

# TC11: countがNone（型不一致）
def test_TC11():
    # TC11
    with pytest.raises(TypeError):
        ProjectHasOpenTicketsError(1, None)

# TC12: project_idとcountが両方str型（型不一致）
def test_TC12():
    # TC12
    with pytest.raises(TypeError):
        ProjectHasOpenTicketsError("1", "5")

# TC13: project_idとcountが両方None（型不一致）
def test_TC13():
    # TC13
    with pytest.raises(TypeError):
        ProjectHasOpenTicketsError(None, None)

# TC17: project_idがstr型、countがNone（型不一致）
def test_TC17():
    # TC17
    with pytest.raises(TypeError):
        ProjectHasOpenTicketsError("1", None)

# TC18: project_idがNone、countがstr型（型不一致）
def test_TC18():
    # TC18
    with pytest.raises(TypeError):
        ProjectHasOpenTicketsError(None, "5")