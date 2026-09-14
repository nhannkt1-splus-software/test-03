import pytest
from functools import partial

# テスト対象クラスのインポート
# from <対象モジュール> import LabelAlreadyAttachedError

# DeskErrorのダミー定義（テスト用）
class DeskError(Exception):
    pass

# テスト対象クラスの再定義（テスト用）
class LabelAlreadyAttachedError(DeskError):
    def __init__(self, ticket_id: int, label_id: int) -> None:
        self.ticket_id = ticket_id
        self.label_id = label_id
        super().__init__(f"Label {label_id} is already on ticket {ticket_id}")

# --- 正常系・境界値・異常系（直接呼び出し） ---
# TC1: ticket_id=1, label_id=2（通常値）
def test_TC1_label_already_attached_error_normal():
    # TC1
    err = LabelAlreadyAttachedError(1, 2)
    assert err.ticket_id == 1  # ticket_idの値確認
    assert err.label_id == 2   # label_idの値確認
    assert str(err) == "Label 2 is already on ticket 1"  # メッセージ確認

# TC2: ticket_id=0, label_id=0（境界値）
def test_TC2_label_already_attached_error_boundary():
    # TC2
    err = LabelAlreadyAttachedError(0, 0)
    assert err.ticket_id == 0
    assert err.label_id == 0
    assert str(err) == "Label 0 is already on ticket 0"

# TC3: ticket_id=-1, label_id=-2（負の値）
def test_TC3_label_already_attached_error_negative():
    # TC3
    err = LabelAlreadyAttachedError(-1, -2)
    assert err.ticket_id == -1
    assert err.label_id == -2
    assert str(err) == "Label -2 is already on ticket -1"

# TC4: ticket_id=999999999, label_id=888888888（大きい値）
def test_TC4_label_already_attached_error_large():
    # TC4
    err = LabelAlreadyAttachedError(999999999, 888888888)
    assert err.ticket_id == 999999999
    assert err.label_id == 888888888
    assert str(err) == "Label 888888888 is already on ticket 999999999"

# --- 型不一致（直接呼び出し） ---
# TC5: ticket_id='1', label_id='2'（str型）
def test_TC5_label_already_attached_error_type_str():
    # TC5
    with pytest.raises(TypeError):
        LabelAlreadyAttachedError('1', '2')

# TC6: ticket_id=None, label_id=2（ticket_idがNone型）
def test_TC6_label_already_attached_error_type_ticket_none():
    # TC6
    with pytest.raises(TypeError):
        LabelAlreadyAttachedError(None, 2)

# TC7: ticket_id=1, label_id=None（label_idがNone型）
def test_TC7_label_already_attached_error_type_label_none():
    # TC7
    with pytest.raises(TypeError):
        LabelAlreadyAttachedError(1, None)

# TC8: ticket_id=None, label_id=None（両方None型）
def test_TC8_label_already_attached_error_type_both_none():
    # TC8
    with pytest.raises(TypeError):
        LabelAlreadyAttachedError(None, None)

# TC9: ticket_id=[], label_id={}（ticket_idがlist型、label_idがdict型）
def test_TC9_label_already_attached_error_type_list_dict():
    # TC9
    with pytest.raises(TypeError):
        LabelAlreadyAttachedError([], {})

# --- 正常系・境界値・異常系（部分適用関数で呼び出し） ---
# TC10: ticket_id=1, label_id=2（通常値、partial）
def test_TC10_label_already_attached_error_normal_partial():
    # TC10
    f = partial(LabelAlreadyAttachedError, 1, 2)
    err = f()
    assert err.ticket_id == 1
    assert err.label_id == 2
    assert str(err) == "Label 2 is already on ticket 1"

# TC11: ticket_id=0, label_id=0（境界値、partial）
def test_TC11_label_already_attached_error_boundary_partial():
    # TC11
    f = partial(LabelAlreadyAttachedError, 0, 0)
    err = f()
    assert err.ticket_id == 0
    assert err.label_id == 0
    assert str(err) == "Label 0 is already on ticket 0"

# TC12: ticket_id=-1, label_id=-2（負の値、partial）
def test_TC12_label_already_attached_error_negative_partial():
    # TC12
    f = partial(LabelAlreadyAttachedError, -1, -2)
    err = f()
    assert err.ticket_id == -1
    assert err.label_id == -2
    assert str(err) == "Label -2 is already on ticket -1"

# TC13: ticket_id=999999999, label_id=888888888（大きい値、partial）
def test_TC13_label_already_attached_error_large_partial():
    # TC13
    f = partial(LabelAlreadyAttachedError, 999999999, 888888888)
    err = f()
    assert err.ticket_id == 999999999
    assert err.label_id == 888888888
    assert str(err) == "Label 888888888 is already on ticket 999999999"

# --- 型不一致（部分適用関数で呼び出し） ---
# TC14: ticket_id='1', label_id='2'（str型、partial）
def test_TC14_label_already_attached_error_type_str_partial():
    # TC14
    f = partial(LabelAlreadyAttachedError, '1', '2')
    with pytest.raises(TypeError):
        f()

# TC15: ticket_id=None, label_id=2（ticket_idがNone型、partial）
def test_TC15_label_already_attached_error_type_ticket_none_partial():
    # TC15
    f = partial(LabelAlreadyAttachedError, None, 2)
    with pytest.raises(TypeError):
        f()

# TC16: ticket_id=1, label_id=None（label_idがNone型、partial）
def test_TC16_label_already_attached_error_type_label_none_partial():
    # TC16
    f = partial(LabelAlreadyAttachedError, 1, None)
    with pytest.raises(TypeError):
        f()

# TC17: ticket_id=None, label_id=None（両方None型、partial）
def test_TC17_label_already_attached_error_type_both_none_partial():
    # TC17
    f = partial(LabelAlreadyAttachedError, None, None)
    with pytest.raises(TypeError):
        f()

# TC18: ticket_id=[], label_id={}（ticket_idがlist型、label_idがdict型、partial）
def test_TC18_label_already_attached_error_type_list_dict_partial():
    # TC18
    f = partial(LabelAlreadyAttachedError, [], {})
    with pytest.raises(TypeError):
        f()