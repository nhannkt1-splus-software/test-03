import pytest

# DeskErrorが未定義の場合、テスト用にダミークラスを定義
try:
    DeskError
except NameError:
    class DeskError(Exception):
        pass

# テスト対象クラスのインポートまたは定義
from types import SimpleNamespace

# テスト対象クラスの再定義（本来はimportで対応）
class InvalidUsernameError(DeskError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f"Invalid username {username}")

# -------------------------------
# TC1: 一般的な有効なユーザー名の文字列
# -------------------------------
def test_invalid_username_error_tc1():
    # TC1
    username = "valid_username"
    err = InvalidUsernameError(username)
    # username属性が正しくセットされているか
    assert err.username == username
    # メッセージが正しいか
    assert str(err) == f"Invalid username {username}"

# -------------------------------
# TC2: 空文字列
# -------------------------------
def test_invalid_username_error_tc2():
    # TC2
    username = ""
    err = InvalidUsernameError(username)
    assert err.username == username
    assert str(err) == "Invalid username "

# -------------------------------
# TC3: 記号を含むユーザー名
# -------------------------------
def test_invalid_username_error_tc3():
    # TC3
    username = "user!@#"
    err = InvalidUsernameError(username)
    assert err.username == username
    assert str(err) == "Invalid username user!@#"

# -------------------------------
# TC4: 1文字のユーザー名
# -------------------------------
def test_invalid_username_error_tc4():
    # TC4
    username = "a"
    err = InvalidUsernameError(username)
    assert err.username == username
    assert str(err) == "Invalid username a"

# -------------------------------
# TC5: 100文字の長いユーザー名
# -------------------------------
def test_invalid_username_error_tc5():
    # TC5
    username = "a" * 100
    err = InvalidUsernameError(username)
    assert err.username == username
    assert str(err) == f"Invalid username {username}"

# -------------------------------
# TC6: None型（型不一致）
# -------------------------------
def test_invalid_username_error_tc6():
    # TC6
    username = None
    err = InvalidUsernameError(username)
    assert err.username is None
    # Noneが文字列化されているか
    assert str(err) == "Invalid username None"

# -------------------------------
# TC7: int型（型不一致）
# -------------------------------
def test_invalid_username_error_tc7():
    # TC7
    username = 123
    err = InvalidUsernameError(username)
    assert err.username == 123
    # intが文字列化されているか
    assert str(err) == "Invalid username 123"

# -------------------------------
# TC8: list型（型不一致）
# -------------------------------
def test_invalid_username_error_tc8():
    # TC8
    username = ["user"]
    err = InvalidUsernameError(username)
    assert err.username == ["user"]
    # listが文字列化されているか
    assert str(err) == "Invalid username ['user']"

# -------------------------------
# TC9: dict型（型不一致）
# -------------------------------
def test_invalid_username_error_tc9():
    # TC9
    username = {"username": "user"}
    err = InvalidUsernameError(username)
    assert err.username == {"username": "user"}
    # dictが文字列化されているか
    assert str(err) == "Invalid username {'username': 'user'}"