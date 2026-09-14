import pytest

# DeskErrorが未定義の場合のため、テスト用にダミークラスを定義
class DeskError(Exception):
    pass

# DuplicateMemberErrorクラスのテスト対象コードをインポートまたは再定義
class DuplicateMemberError(DeskError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f"Member {username} already exists")

# --- 正常系テスト ---

# TC1: 通常のユーザー名
def test_duplicate_member_error_tc1():
    # TC1
    username = "user1"
    err = DuplicateMemberError(username)
    # エラーメッセージの検証
    assert str(err) == "Member user1 already exists"
    # username属性の検証
    assert err.username == username

# TC2: 空文字列のユーザー名
def test_duplicate_member_error_tc2():
    # TC2
    username = ""
    err = DuplicateMemberError(username)
    assert str(err) == "Member  already exists"
    assert err.username == username

# TC3: 1文字のユーザー名
def test_duplicate_member_error_tc3():
    # TC3
    username = "a"
    err = DuplicateMemberError(username)
    assert str(err) == "Member a already exists"
    assert err.username == username

# TC4: 100文字のユーザー名
def test_duplicate_member_error_tc4():
    # TC4
    username = "a" * 100
    err = DuplicateMemberError(username)
    assert str(err) == f"Member {username} already exists"
    assert err.username == username

# TC5: 特殊文字を含むユーザー名
def test_duplicate_member_error_tc5():
    # TC5
    username = "user@name"
    err = DuplicateMemberError(username)
    assert str(err) == "Member user@name already exists"
    assert err.username == username

# TC10: 空白のみのユーザー名
def test_duplicate_member_error_tc10():
    # TC10
    username = "   "
    err = DuplicateMemberError(username)
    assert str(err) == "Member    already exists"
    assert err.username == username

# TC11: 日本語を含むユーザー名
def test_duplicate_member_error_tc11():
    # TC11
    username = "ユーザー名"
    err = DuplicateMemberError(username)
    assert str(err) == "Member ユーザー名 already exists"
    assert err.username == username

# TC12: 改行を含むユーザー名
def test_duplicate_member_error_tc12():
    # TC12
    username = "user\nname"
    err = DuplicateMemberError(username)
    assert str(err) == "Member user\nname already exists"
    assert err.username == username

# TC13: タブ文字を含むユーザー名
def test_duplicate_member_error_tc13():
    # TC13
    username = "user\tname"
    err = DuplicateMemberError(username)
    assert str(err) == "Member user\tname already exists"
    assert err.username == username

# --- 異常系テスト ---

# TC6: int型（型不一致）
def test_duplicate_member_error_tc6():
    # TC6
    username = 123
    with pytest.raises(TypeError):
        DuplicateMemberError(username)

# TC7: NoneType（型不一致）
def test_duplicate_member_error_tc7():
    # TC7
    username = None
    with pytest.raises(TypeError):
        DuplicateMemberError(username)

# TC8: list型（型不一致）
def test_duplicate_member_error_tc8():
    # TC8
    username = []
    with pytest.raises(TypeError):
        DuplicateMemberError(username)

# TC9: dict型（型不一致）
def test_duplicate_member_error_tc9():
    # TC9
    username = {}
    with pytest.raises(TypeError):
        DuplicateMemberError(username)