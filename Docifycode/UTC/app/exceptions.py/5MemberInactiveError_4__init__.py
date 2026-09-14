import pytest

# DeskErrorのダミークラスを定義（テスト用）
class DeskError(Exception):
    pass

# テスト対象クラスのインポートまたは再定義
class MemberInactiveError(DeskError):

    # テスト対象メソッド
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f"Member {username} is inactive")

# --- 正常系テスト ---

# TC1: 一般的な英数字のユーザー名
def test_member_inactive_error_tc1():
    # TC1
    username = "user123"
    err = MemberInactiveError(username)
    # username属性が正しくセットされていることを確認
    assert err.username == username
    # エラーメッセージが正しいことを確認
    assert str(err) == "Member user123 is inactive"

# TC2: 空文字列のユーザー名
def test_member_inactive_error_tc2():
    # TC2
    username = ""
    err = MemberInactiveError(username)
    assert err.username == username
    assert str(err) == "Member  is inactive"

# TC3: 特殊文字を含むユーザー名
def test_member_inactive_error_tc3():
    # TC3
    username = "ユーザー名_特殊文字!@#"
    err = MemberInactiveError(username)
    assert err.username == username
    assert str(err) == "Member ユーザー名_特殊文字!@# is inactive"

# TC4: 1文字のユーザー名（境界値）
def test_member_inactive_error_tc4():
    # TC4
    username = "a"
    err = MemberInactiveError(username)
    assert err.username == username
    assert str(err) == "Member a is inactive"

# TC5: 100文字の長いユーザー名（境界値）
def test_member_inactive_error_tc5():
    # TC5
    username = "a" * 100
    err = MemberInactiveError(username)
    assert err.username == username
    assert str(err) == f"Member {username} is inactive"

# --- 異常系テスト ---

# TC6: int型のユーザー名（型不一致）
def test_member_inactive_error_tc6():
    # TC6
    username = 123
    with pytest.raises(TypeError):
        MemberInactiveError(username)

# TC7: None型のユーザー名（型不一致）
def test_member_inactive_error_tc7():
    # TC7
    username = None
    with pytest.raises(TypeError):
        MemberInactiveError(username)

# TC8: list型のユーザー名（型不一致）
def test_member_inactive_error_tc8():
    # TC8
    username = []
    with pytest.raises(TypeError):
        MemberInactiveError(username)

# TC9: dict型のユーザー名（型不一致）
def test_member_inactive_error_tc9():
    # TC9
    username = {}
    with pytest.raises(TypeError):
        MemberInactiveError(username)
```
