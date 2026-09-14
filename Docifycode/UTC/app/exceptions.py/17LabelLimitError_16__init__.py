import pytest

# LabelLimitErrorのインポートを想定
# from your_module import LabelLimitError

# DeskErrorのダミークラスを用意（テスト用: 実際の環境では不要）
class DeskError(Exception):
    pass

# テスト対象クラスの再定義（実際のテストではインポートして使用）
class LabelLimitError(DeskError):
    def __init__(self, ticket_id: int, limit: int) -> None:
        self.ticket_id = ticket_id
        self.limit = limit
        super().__init__(f"Ticket {ticket_id} already has {limit} labels")

# --- 正常系 ---

# TC1: ticket_id, limitともにint型の正常値
def test_label_limit_error_tc1():
    # TC1
    ticket_id = 1
    limit = 5
    err = LabelLimitError(ticket_id, limit)
    # ticket_id, limit属性の値を確認
    assert err.ticket_id == ticket_id
    assert err.limit == limit
    # メッセージ内容を確認
    assert str(err) == "Ticket 1 already has 5 labels"

# TC2: ticket_id, limitともに0（境界値）
def test_label_limit_error_tc2():
    # TC2
    ticket_id = 0
    limit = 0
    err = LabelLimitError(ticket_id, limit)
    assert err.ticket_id == ticket_id
    assert err.limit == limit
    assert str(err) == "Ticket 0 already has 0 labels"

# TC3: ticket_idが負の値
def test_label_limit_error_tc3():
    # TC3
    ticket_id = -1
    limit = 3
    err = LabelLimitError(ticket_id, limit)
    assert err.ticket_id == ticket_id
    assert err.limit == limit
    assert str(err) == "Ticket -1 already has 3 labels"

# TC4: ticket_id, limitともに大きな値
def test_label_limit_error_tc4():
    # TC4
    ticket_id = 1000000
    limit = 100
    err = LabelLimitError(ticket_id, limit)
    assert err.ticket_id == ticket_id
    assert err.limit == limit
    assert str(err) == "Ticket 1000000 already has 100 labels"

# --- 異常系（型違い） ---

# TC5: ticket_idがstr型
def test_label_limit_error_tc5():
    # TC5
    ticket_id = '1'
    limit = 5
    err = LabelLimitError(ticket_id, limit)
    # ticket_id, limit属性の値を確認
    assert err.ticket_id == ticket_id
    assert err.limit == limit
    # メッセージ内容を確認
    assert str(err) == "Ticket 1 already has 5 labels"

# TC6: limitがstr型
def test_label_limit_error_tc6():
    # TC6
    ticket_id = 1
    limit = '5'
    err = LabelLimitError(ticket_id, limit)
    assert err.ticket_id == ticket_id
    assert err.limit == limit
    assert str(err) == "Ticket 1 already has 5 labels"

# TC7: ticket_idがNone
def test_label_limit_error_tc7():
    # TC7
    ticket_id = None
    limit = 5
    err = LabelLimitError(ticket_id, limit)
    assert err.ticket_id is None
    assert err.limit == limit
    assert str(err) == "Ticket None already has 5 labels"

# TC8: limitがNone
def test_label_limit_error_tc8():
    # TC8
    ticket_id = 1
    limit = None
    err = LabelLimitError(ticket_id, limit)
    assert err.ticket_id == ticket_id
    assert err.limit is None
    assert str(err) == "Ticket 1 already has None labels"

# TC9: ticket_id, limitともにNone
def test_label_limit_error_tc9():
    # TC9
    ticket_id = None
    limit = None
    err = LabelLimitError(ticket_id, limit)
    assert err.ticket_id is None
    assert err.limit is None
    assert str(err) == "Ticket None already has None labels"

# TC10: ticket_idがdict型、limitがlist型
def test_label_limit_error_tc10():
    # TC10
    ticket_id = []
    limit = {}
    err = LabelLimitError(ticket_id, limit)
    assert err.ticket_id == ticket_id
    assert err.limit == limit
    # str([]) = '[]', str({}) = '{}'
    assert str(err) == "Ticket [] already has {} labels"
```
