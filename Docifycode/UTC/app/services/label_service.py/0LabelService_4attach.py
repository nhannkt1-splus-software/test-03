import pytest

# --- テスト用ダミークラス・例外定義 ---
# Ticket, Label, 例外クラスをテスト用に定義
class Ticket:
    def __init__(self, id, label_ids):
        self.id = id
        self.label_ids = label_ids

class Label:
    def __init__(self, id):
        self.id = id

class LabelAlreadyAttachedError(Exception):
    def __init__(self, ticket_id, label_id):
        self.ticket_id = ticket_id
        self.label_id = label_id

class LabelLimitError(Exception):
    def __init__(self, ticket_id, max_labels):
        self.ticket_id = ticket_id
        self.max_labels = max_labels

class TicketNotFoundError(Exception):
    pass

class LabelNotFoundError(Exception):
    pass

# --- テスト対象クラスのインポート ---
# MAX_LABELS_PER_TICKETをテストごとに設定するため、グローバル変数として扱う
import sys

# テスト対象クラスのスコープにMAX_LABELS_PER_TICKETを注入
def set_max_labels_per_ticket(val):
    sys.modules[__name__].MAX_LABELS_PER_TICKET = val

# --- LabelServiceのテスト用サブクラス ---
# _get_writable_ticket, get_labelをテスト用にモックする
from types import MethodType

@pytest.fixture
def label_service():
    from target import LabelService  # テスト対象クラスをインポート（必要に応じてパスを修正）
    return LabelService()

# --- テストケース ---
# TC1: 正常系：ラベル未付与のチケットに新しいラベルを付与するケース
def test_attach_TC1(monkeypatch):
    # テストID: TC1
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    ticket = Ticket(ticket_id, [])
    label = Label(label_id)

    # _get_writable_ticketのモック
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    # get_labelのモック
    monkeypatch.setattr(service, "get_label", lambda lid: label)

    result = service.attach(ticket_id, label_id)
    # チケットにラベルが追加されていることを確認
    assert label_id in result.label_ids
    assert result.id == ticket_id

# TC2: 異常系：既にラベルが付与されている場合
def test_attach_TC2(monkeypatch):
    # テストID: TC2
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    ticket = Ticket(ticket_id, [10])
    label = Label(label_id)

    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)

    with pytest.raises(LabelAlreadyAttachedError) as e:
        service.attach(ticket_id, label_id)
    assert e.value.ticket_id == ticket_id
    assert e.value.label_id == label_id

# TC3: 異常系：ラベル上限に達している場合
def test_attach_TC3(monkeypatch):
    # テストID: TC3
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    ticket = Ticket(ticket_id, [1,2,3,4,5])
    label = Label(label_id)

    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)

    with pytest.raises(LabelLimitError) as e:
        service.attach(ticket_id, label_id)
    assert e.value.ticket_id == ticket_id
    assert e.value.max_labels == 5

# TC4: 正常系：ラベル上限直前のチケットに新しいラベルを付与するケース
def test_attach_TC4(monkeypatch):
    # テストID: TC4
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    ticket = Ticket(ticket_id, [1,2,3,4])
    label = Label(label_id)

    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)

    result = service.attach(ticket_id, label_id)
    assert label_id in result.label_ids
    assert result.id == ticket_id

# TC5: 正常系：ticket_id, label_idの境界値（0）
def test_attach_TC5(monkeypatch):
    # テストID: TC5
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 0
    label_id = 0
    ticket = Ticket(ticket_id, [])
    label = Label(label_id)

    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)

    result = service.attach(ticket_id, label_id)
    assert label_id in result.label_ids
    assert result.id == ticket_id

# TC6: 正常系：ticket_id, label_idが負の値
def test_attach_TC6(monkeypatch):
    # テストID: TC6
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = -1
    label_id = -5
    ticket = Ticket(ticket_id, [])
    label = Label(label_id)

    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)

    result = service.attach(ticket_id, label_id)
    assert label_id in result.label_ids
    assert result.id == ticket_id

# TC7: 正常系：ticket_id, label_idが非常に大きい値
def test_attach_TC7(monkeypatch):
    # テストID: TC7
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 999999
    label_id = 888888
    ticket = Ticket(ticket_id, [])
    label = Label(label_id)

    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)

    result = service.attach(ticket_id, label_id)
    assert label_id in result.label_ids
    assert result.id == ticket_id

# TC8: 異常系：ticket_id, label_idがstr型（型不一致）
@pytest.mark.parametrize("ticket_id,label_id", [
    ("1", "10"),
])
def test_attach_TC8(monkeypatch, ticket_id, label_id):
    # テストID: TC8
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    # 型不一致なので例外が発生することを期待
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: Ticket(tid, []))
    monkeypatch.setattr(service, "get_label", lambda lid: Label(lid))
    with pytest.raises(TypeError):
        service.attach(ticket_id, label_id)

# TC9: 異常系：ticket_id, label_idがNone（型不一致）
@pytest.mark.parametrize("ticket_id,label_id", [
    (None, None),
])
def test_attach_TC9(monkeypatch, ticket_id, label_id):
    # テストID: TC9
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: Ticket(tid, []))
    monkeypatch.setattr(service, "get_label", lambda lid: Label(lid))
    with pytest.raises(TypeError):
        service.attach(ticket_id, label_id)

# TC10: 異常系：ticket_id, label_idがfloat型（型不一致）
@pytest.mark.parametrize("ticket_id,label_id", [
    (1.5, 2.5),
])
def test_attach_TC10(monkeypatch, ticket_id, label_id):
    # テストID: TC10
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: Ticket(tid, []))
    monkeypatch.setattr(service, "get_label", lambda lid: Label(lid))
    with pytest.raises(TypeError):
        service.attach(ticket_id, label_id)

# TC11: 異常系：ticket_idがlist, label_idがdict（型不一致）
@pytest.mark.parametrize("ticket_id,label_id", [
    ([], {}),
])
def test_attach_TC11(monkeypatch, ticket_id, label_id):
    # テストID: TC11
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: Ticket(tid, []))
    monkeypatch.setattr(service, "get_label", lambda lid: Label(lid))
    with pytest.raises(TypeError):
        service.attach(ticket_id, label_id)

# TC12: 異常系：ticket_idが存在しない場合
def test_attach_TC12(monkeypatch):
    # テストID: TC12
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    # _get_writable_ticketでTicketNotFoundErrorを発生させる
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: (_ for _ in ()).throw(TicketNotFoundError()))
    monkeypatch.setattr(service, "get_label", lambda lid: Label(label_id))
    with pytest.raises(TicketNotFoundError):
        service.attach(ticket_id, label_id)

# TC13: 異常系：label_idが存在しない場合
def test_attach_TC13(monkeypatch):
    # テストID: TC13
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: Ticket(ticket_id, []))
    # get_labelでLabelNotFoundErrorを発生させる
    monkeypatch.setattr(service, "get_label", lambda lid: (_ for _ in ()).throw(LabelNotFoundError()))
    with pytest.raises(LabelNotFoundError):
        service.attach(ticket_id, label_id)

# TC14: 異常系：ラベル上限に達しており、付与しようとするラベルが未付与の場合
def test_attach_TC14(monkeypatch):
    # テストID: TC14
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    ticket = Ticket(ticket_id, [10, 20, 30, 40, 50])
    label = Label(label_id)
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)
    with pytest.raises(LabelLimitError) as e:
        service.attach(ticket_id, label_id)
    assert e.value.ticket_id == ticket_id
    assert e.value.max_labels == 5

# TC15: 正常系：上限直前で付与しようとするラベルが未付与の場合
def test_attach_TC15(monkeypatch):
    # テストID: TC15
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    ticket = Ticket(ticket_id, [10, 20, 30, 40])
    label = Label(label_id)
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)
    result = service.attach(ticket_id, label_id)
    assert label_id in result.label_ids
    assert result.id == ticket_id

# TC16: 正常系：既存ラベルが4つで新しいラベルを付与するケース
def test_attach_TC16(monkeypatch):
    # テストID: TC16
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    ticket = Ticket(ticket_id, [20, 30, 40, 50])
    label = Label(label_id)
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)
    result = service.attach(ticket_id, label_id)
    assert label_id in result.label_ids
    assert result.id == ticket_id

# TC17: 異常系：ラベル上限に達していて、付与しようとするラベルが既に付与されている場合
def test_attach_TC17(monkeypatch):
    # テストID: TC17
    set_max_labels_per_ticket(5)
    from target import LabelService
    service = LabelService()
    ticket_id = 1
    label_id = 10
    ticket = Ticket(ticket_id, [10, 20, 30, 40, 50])
    label = Label(label_id)
    monkeypatch.setattr(service, "_get_writable_ticket", lambda tid: ticket)
    monkeypatch.setattr(service, "get_label", lambda lid: label)
    with pytest.raises(LabelAlreadyAttachedError) as e:
        service.attach(ticket_id, label_id)
    assert e.value.ticket_id == ticket_id
    assert e.value.label_id == label_id