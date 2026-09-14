import pytest

# DeskErrorが未定義の場合、テスト用にダミー定義
class DeskError(Exception):
    pass

# MemberHasActiveTicketsErrorクラスのテスト対象
from types import SimpleNamespace

# テスト対象クラスの定義（本来はimportで取得）
class MemberHasActiveTicketsError(DeskError):
    def __init__(self, username: str, count: int) -> None:
        self.username = username
        self.count = count
        super().__init__(f"Cannot deactivate {username}: {count} active ticket(s)")

# --- 正常系テスト ---

# TC1: 一般的なユーザー名と1件のチケット
def test_TC1_member_has_active_tickets_error_normal():
    # TC1
    username = "valid_username"
    count = 1
    err = MemberHasActiveTicketsError(username, count)
    # usernameとcountが正しくセットされていることを確認
    assert err.username == username  # TC1
    assert err.count == count        # TC1
    # エラーメッセージが正しいことを確認
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC1

# TC2: 空文字列のユーザー名
def test_TC2_member_has_active_tickets_error_empty_username():
    # TC2
    username = ""
    count = 1
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC2
    assert err.count == count        # TC2
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC2

# TC3: 特殊文字を含むユーザー名
def test_TC3_member_has_active_tickets_error_special_username():
    # TC3
    username = "ユーザー名に特殊文字!@#"
    count = 1
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC3
    assert err.count == count        # TC3
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC3

# TC4: 100文字の長いユーザー名
def test_TC4_member_has_active_tickets_error_long_username():
    # TC4
    username = "a" * 100
    count = 1
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC4
    assert err.count == count        # TC4
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC4

# TC5: チケット数が0（境界値）
def test_TC5_member_has_active_tickets_error_count_zero():
    # TC5
    username = "valid_username"
    count = 0
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC5
    assert err.count == count        # TC5
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC5

# TC6: チケット数が100（多い件数の境界値）
def test_TC6_member_has_active_tickets_error_count_100():
    # TC6
    username = "valid_username"
    count = 100
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC6
    assert err.count == count        # TC6
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC6

# TC7: チケット数が負の値（異常値だが型は正しい）
def test_TC7_member_has_active_tickets_error_count_negative():
    # TC7
    username = "valid_username"
    count = -1
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC7
    assert err.count == count        # TC7
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC7

# TC13: 空文字列のユーザー名かつチケット数が0（境界値組み合わせ）
def test_TC13_member_has_active_tickets_error_empty_username_and_count_zero():
    # TC13
    username = ""
    count = 0
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC13
    assert err.count == count        # TC13
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC13

# TC14: 特殊文字を含むユーザー名かつチケット数が多い（組み合わせ）
def test_TC14_member_has_active_tickets_error_special_username_and_count_100():
    # TC14
    username = "ユーザー名に特殊文字!@#"
    count = 100
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC14
    assert err.count == count        # TC14
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC14

# TC15: 100文字の長いユーザー名かつチケット数が0（境界値組み合わせ）
def test_TC15_member_has_active_tickets_error_long_username_and_count_zero():
    # TC15
    username = "a" * 100
    count = 0
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC15
    assert err.count == count        # TC15
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC15

# TC16: 100文字の長いユーザー名かつチケット数が負の値（異常値組み合わせ）
def test_TC16_member_has_active_tickets_error_long_username_and_count_negative():
    # TC16
    username = "a" * 100
    count = -1
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC16
    assert err.count == count        # TC16
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC16

# TC17: 特殊文字を含むユーザー名かつチケット数が負の値（異常値組み合わせ）
def test_TC17_member_has_active_tickets_error_special_username_and_count_negative():
    # TC17
    username = "ユーザー名に特殊文字!@#"
    count = -1
    err = MemberHasActiveTicketsError(username, count)
    assert err.username == username  # TC17
    assert err.count == count        # TC17
    assert str(err) == f"Cannot deactivate {username}: {count} active ticket(s)"  # TC17

# --- 異常系テスト ---

# TC8: usernameがint型（型不一致）
def test_TC8_member_has_active_tickets_error_username_int_typeerror():
    # TC8
    username = 123
    count = 1
    with pytest.raises(TypeError):  # TC8
        MemberHasActiveTicketsError(username, count)

# TC9: usernameがNone型（型不一致）
def test_TC9_member_has_active_tickets_error_username_none_typeerror():
    # TC9
    username = None
    count = 1
    with pytest.raises(TypeError):  # TC9
        MemberHasActiveTicketsError(username, count)

# TC10: countがNone型（型不一致）
def test_TC10_member_has_active_tickets_error_count_none_typeerror():
    # TC10
    username = "valid_username"
    count = None
    with pytest.raises(TypeError):  # TC10
        MemberHasActiveTicketsError(username, count)

# TC11: countがstr型（型不一致）
def test_TC11_member_has_active_tickets_error_count_str_typeerror():
    # TC11
    username = "valid_username"
    count = "10"
    with pytest.raises(TypeError):  # TC11
        MemberHasActiveTicketsError(username, count)

# TC12: countがfloat型（型不一致）
def test_TC12_member_has_active_tickets_error_count_float_typeerror():
    # TC12
    username = "valid_username"
    count = 0.5
    with pytest.raises(TypeError):  # TC12
        MemberHasActiveTicketsError(username, count)