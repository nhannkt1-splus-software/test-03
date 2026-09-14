import pytest

# テスト用のTicketクラスを定義
class Ticket:
    def __init__(self, label_ids=None):
        self.label_ids = label_ids if label_ids is not None else []

# テスト用のLabelServiceのサブクラスを作成し、必要なメソッドをモック
class TestableLabelService(LabelService):
    def __init__(self, tickets=None, labels=None, raise_ticket_error=None, raise_label_error=None, ticket_has_no_label_ids=False):
        # tickets: {ticket_id: Ticket}
        # labels: set(label_id)
        self._tickets = tickets if tickets is not None else {}
        self._labels = labels if labels is not None else set()
        self._raise_ticket_error = raise_ticket_error
        self._raise_label_error = raise_label_error
        self._ticket_has_no_label_ids = ticket_has_no_label_ids

    def _get_writable_ticket(self, ticket_id):
        # 型チェック
        if not isinstance(ticket_id, int):
            raise TypeError("ticket_id must be int")
        if ticket_id is None:
            raise TypeError("ticket_id must not be None")
        if self._raise_ticket_error == 'attribute':
            raise AttributeError("Ticket instance cannot be retrieved")
        if ticket_id not in self._tickets or ticket_id <= 0:
            raise ValueError("ticket_id does not exist")
        ticket = self._tickets[ticket_id]
        if self._ticket_has_no_label_ids:
            delattr(ticket, 'label_ids')
        return ticket

    def get_label(self, label_id):
        # 型チェック
        if not isinstance(label_id, int):
            raise TypeError("label_id must be int")
        if label_id is None:
            raise TypeError("label_id must not be None")
        if self._raise_label_error == 'attribute':
            raise AttributeError("Label instance cannot be retrieved")
        if label_id not in self._labels or label_id <= 0:
            raise ValueError("label_id does not exist")
        return label_id

# --- テストケース ---

# TC1: label_idがticket.label_idsに含まれている場合
def test_detach_TC1():
    # TC1
    tickets = {1: Ticket([1, 2, 3])}
    labels = {1, 2, 3}
    service = TestableLabelService(tickets=tickets, labels=labels)
    ticket = service.detach(1, 2)
    # 2が削除されていることを確認
    assert ticket.label_ids == [1, 3]

# TC2: label_idがticket.label_idsに含まれていない場合
def test_detach_TC2():
    # TC2
    tickets = {1: Ticket([1, 3])}
    labels = {1, 2, 3, 99}
    service = TestableLabelService(tickets=tickets, labels=labels)
    ticket = service.detach(1, 99)
    # label_idsに変更なし
    assert ticket.label_ids == [1, 3]

# TC3: ticket_idが存在しない場合
def test_detach_TC3():
    # TC3
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(ValueError):
        service.detach(999, 2)

# TC4: label_idが存在しない場合
def test_detach_TC4():
    # TC4
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(ValueError):
        service.detach(1, 999)

# TC5: ticket.label_idsが空リストの場合
def test_detach_TC5():
    # TC5
    tickets = {1: Ticket([])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    ticket = service.detach(1, 2)
    assert ticket.label_ids == []

# TC6: ticket.label_idsが複数のlabel_idを含む場合
def test_detach_TC6():
    # TC6
    tickets = {1: Ticket([1, 2, 3, 4])}
    labels = {1, 2, 3, 4}
    service = TestableLabelService(tickets=tickets, labels=labels)
    ticket = service.detach(1, 2)
    assert ticket.label_ids == [1, 3, 4]

# TC7: ticket.label_idsに重複したlabel_idが含まれている場合
def test_detach_TC7():
    # TC7
    tickets = {1: Ticket([2, 2, 1, 2, 3])}
    labels = {1, 2, 3}
    service = TestableLabelService(tickets=tickets, labels=labels)
    ticket = service.detach(1, 2)
    assert ticket.label_ids == [1, 3]

# TC8: ticket_idがint型でない場合
def test_detach_TC8():
    # TC8
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(TypeError):
        service.detach("a", 2)

# TC9: label_idがint型でない場合
def test_detach_TC9():
    # TC9
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(TypeError):
        service.detach(1, "b")

# TC10: ticket_idがNoneの場合
def test_detach_TC10():
    # TC10
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(TypeError):
        service.detach(None, 2)

# TC11: label_idがNoneの場合
def test_detach_TC11():
    # TC11
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(TypeError):
        service.detach(1, None)

# TC12: _get_writable_ticketがAttributeErrorを投げる場合
def test_detach_TC12():
    # TC12
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels, raise_ticket_error='attribute')
    with pytest.raises(AttributeError):
        service.detach(1, 2)

# TC13: ticket.label_idsが存在しない場合
def test_detach_TC13():
    # TC13
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels, ticket_has_no_label_ids=True)
    with pytest.raises(AttributeError):
        service.detach(1, 2)

# TC14: label_idが負の値で存在しない場合
def test_detach_TC14():
    # TC14
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(ValueError):
        service.detach(1, -1)

# TC15: ticket_idが負の値で存在しない場合
def test_detach_TC15():
    # TC15
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(ValueError):
        service.detach(-1, 2)

# TC16: ticket.label_idsが大量のlabel_idを含む場合
def test_detach_TC16():
    # TC16
    label_ids = [2] * 500 + [1] * 250 + [3] * 250
    tickets = {1: Ticket(label_ids)}
    labels = {1, 2, 3}
    service = TestableLabelService(tickets=tickets, labels=labels)
    ticket = service.detach(1, 2)
    # 2が全て削除されていることを確認
    assert ticket.label_ids == [1] * 250 + [3] * 250

# TC17: label_idが0の場合
def test_detach_TC17():
    # TC17
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(ValueError):
        service.detach(1, 0)

# TC18: ticket_idが0の場合
def test_detach_TC18():
    # TC18
    tickets = {1: Ticket([1, 2])}
    labels = {1, 2}
    service = TestableLabelService(tickets=tickets, labels=labels)
    with pytest.raises(ValueError):
        service.detach(0, 2)