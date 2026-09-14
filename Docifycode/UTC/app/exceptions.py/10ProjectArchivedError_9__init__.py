import pytest

# DeskErrorのダミークラスを定義（テスト用）
class DeskError(Exception):
    pass

# テスト対象クラスのインポートまたは再定義
from types import SimpleNamespace

# ProjectArchivedErrorクラスの再定義（テスト対象コードをそのまま利用）
class ProjectArchivedError(DeskError):
    def __init__(self, project_id: int, action: str) -> None:
        self.project_id = project_id
        self.action = action
        super().__init__(f"Cannot {action} archived project {project_id}")

# --- テストケース ---

# TC1: 正常系：project_idが正の整数、actionが一般的な文字列
def test_TC1():
    # TC1
    err = ProjectArchivedError(1, "delete")
    # メッセージと属性を検証
    assert str(err) == "Cannot delete archived project 1"
    assert err.project_id == 1
    assert err.action == "delete"

# TC2: 境界値テスト：project_idが0
def test_TC2():
    # TC2
    err = ProjectArchivedError(0, "update")
    assert str(err) == "Cannot update archived project 0"
    assert err.project_id == 0
    assert err.action == "update"

# TC3: 異常値テスト：project_idが負の整数
def test_TC3():
    # TC3
    err = ProjectArchivedError(-1, "delete")
    assert str(err) == "Cannot delete archived project -1"
    assert err.project_id == -1
    assert err.action == "delete"

# TC4: 大きな値テスト：project_idが非常に大きい整数
def test_TC4():
    # TC4
    err = ProjectArchivedError(999999999, "update")
    assert str(err) == "Cannot update archived project 999999999"
    assert err.project_id == 999999999
    assert err.action == "update"

# TC5: 型不一致：project_idがstr型
def test_TC5():
    # TC5
    err = ProjectArchivedError("1", "delete")
    assert str(err) == "Cannot delete archived project 1"
    assert err.project_id == "1"
    assert err.action == "delete"

# TC6: 型不一致：project_idがNone
def test_TC6():
    # TC6
    err = ProjectArchivedError(None, "delete")
    assert str(err) == "Cannot delete archived project None"
    assert err.project_id is None
    assert err.action == "delete"

# TC7: 型不一致：project_idがfloat型
def test_TC7():
    # TC7
    err = ProjectArchivedError(3.14, "delete")
    assert str(err) == "Cannot delete archived project 3.14"
    assert err.project_id == 3.14
    assert err.action == "delete"

# TC8: 型不一致：project_idがリスト型
def test_TC8():
    # TC8
    err = ProjectArchivedError([], "delete")
    assert str(err) == "Cannot delete archived project []"
    assert err.project_id == []
    assert err.action == "delete"

# TC9: 型不一致：project_idが辞書型
def test_TC9():
    # TC9
    err = ProjectArchivedError({}, "delete")
    assert str(err) == "Cannot delete archived project {}"
    assert err.project_id == {}
    assert err.action == "delete"

# TC10: 異常値テスト：actionが空文字列
def test_TC10():
    # TC10
    err = ProjectArchivedError(1, "")
    assert str(err) == "Cannot  archived project 1"
    assert err.project_id == 1
    assert err.action == ""

# TC11: 多言語対応テスト：actionが日本語
def test_TC11():
    # TC11
    err = ProjectArchivedError(1, "アーカイブ")
    assert str(err) == "Cannot アーカイブ archived project 1"
    assert err.project_id == 1
    assert err.action == "アーカイブ"

# TC12: 特殊文字テスト：actionが特殊文字
def test_TC12():
    # TC12
    err = ProjectArchivedError(1, "!@#$%^&*()")
    assert str(err) == "Cannot !@#$%^&*() archived project 1"
    assert err.project_id == 1
    assert err.action == "!@#$%^&*()"

# TC13: 型不一致：actionがNone
def test_TC13():
    # TC13
    err = ProjectArchivedError(1, None)
    assert str(err) == "Cannot None archived project 1"
    assert err.project_id == 1
    assert err.action is None

# TC14: 型不一致：actionがint型
def test_TC14():
    # TC14
    err = ProjectArchivedError(1, 123)
    assert str(err) == "Cannot 123 archived project 1"
    assert err.project_id == 1
    assert err.action == 123

# TC15: 型不一致：actionがリスト型
def test_TC15():
    # TC15
    err = ProjectArchivedError(1, [])
    assert str(err) == "Cannot [] archived project 1"
    assert err.project_id == 1
    assert err.action == []

# TC16: 境界値と異常値の組み合わせ：project_idが0、actionが空文字列
def test_TC16():
    # TC16
    err = ProjectArchivedError(0, "")
    assert str(err) == "Cannot  archived project 0"
    assert err.project_id == 0
    assert err.action == ""

# TC17: 異常値と多言語対応の組み合わせ：project_idが負の整数、actionが日本語
def test_TC17():
    # TC17
    err = ProjectArchivedError(-1, "アーカイブ")
    assert str(err) == "Cannot アーカイブ archived project -1"
    assert err.project_id == -1
    assert err.action == "アーカイブ"

# TC18: 大きな値と特殊文字の組み合わせ：project_idが非常に大きい整数、actionが特殊文字
def test_TC18():
    # TC18
    err = ProjectArchivedError(999999999, "!@#$%^&*()")
    assert str(err) == "Cannot !@#$%^&*() archived project 999999999"
    assert err.project_id == 999999999
    assert err.action == "!@#$%^&*()"

# TC19: 型不一致：project_idとaction両方が型不一致
def test_TC19():
    # TC19
    err = ProjectArchivedError("1", None)
    assert str(err) == "Cannot None archived project 1"
    assert err.project_id == "1"
    assert err.action is None

# TC20: 型不一致：project_idとaction両方が型不一致
def test_TC20():
    # TC20
    err = ProjectArchivedError(None, 123)
    assert str(err) == "Cannot 123 archived project None"
    assert err.project_id is None
    assert err.action == 123

# TC21: 型不一致：project_idとaction両方が型不一致
def test_TC21():
    # TC21
    err = ProjectArchivedError(3.14, [])
    assert str(err) == "Cannot [] archived project 3.14"
    assert err.project_id == 3.14
    assert err.action == []

# TC22: 型不一致：project_idがリスト型、actionが日本語
def test_TC22():
    # TC22
    err = ProjectArchivedError([], "アーカイブ")
    assert str(err) == "Cannot アーカイブ archived project []"
    assert err.project_id == []
    assert err.action == "アーカイブ"

# TC23: 型不一致：project_idが辞書型、actionが特殊文字
def test_TC23():
    # TC23
    err = ProjectArchivedError({}, "!@#$%^&*()")
    assert str(err) == "Cannot !@#$%^&*() archived project {}"
    assert err.project_id == {}
    assert err.action == "!@#$%^&*()"