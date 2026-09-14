import pytest

# テスト対象関数と依存関数・クラスのインポート
from fastapi import HTTPException
from target_module import detach_label, DeskError, to_ticket_out, TicketOut

# LabelServiceのモッククラス
class MockLabelService:
    def __init__(self, detach_behavior=None):
        self.detach_behavior = detach_behavior

    def detach(self, ticket_id, label_id):
        if callable(self.detach_behavior):
            return self.detach_behavior(ticket_id, label_id)
        return self.detach_behavior

# http_errorのモック
def mock_http_error(exc):
    raise HTTPException(status_code=400, detail=str(exc))

# to_ticket_outのモック
def mock_to_ticket_out(ticket):
    if ticket is None or not isinstance(ticket, TicketOut):
        raise TypeError("Invalid ticket")
    return ticket

# TicketOutのモック
class MockTicketOut(TicketOut):
    pass

# DeskErrorのモック
class MockDeskError(DeskError):
    pass

# detach_labelの依存関数を差し替えるヘルパー
def call_detach_label(ticket_id, label_id, service):
    # detach_labelのDependsを無視して直接渡す
    # to_ticket_out, http_errorも差し替え
    # ここではglobals()で差し替え
    orig_to_ticket_out = detach_label.__globals__['to_ticket_out']
    orig_http_error = detach_label.__globals__['http_error']
    detach_label.__globals__['to_ticket_out'] = mock_to_ticket_out
    detach_label.__globals__['http_error'] = mock_http_error
    try:
        return detach_label(ticket_id, label_id, service)
    finally:
        detach_label.__globals__['to_ticket_out'] = orig_to_ticket_out
        detach_label.__globals__['http_error'] = orig_http_error

# --- TC1: 正常系 ---
def test_detach_label_TC1():
    # TC1: detachが正常に動作
    # チケットID・ラベルIDともに有効な値
    # 期待される結果: None（to_ticket_outがMockTicketOutを返す）
    # 日本語コメント: TC1
    service = MockLabelService(detach_behavior=MockTicketOut())
    result = call_detach_label(1, 1, service)
    assert isinstance(result, MockTicketOut)

# --- TC2: 異常系 存在しないチケットID ---
def test_detach_label_TC2():
    # TC2: detachがDeskErrorを発生
    # ticket_id=0
    # 期待される結果: HTTPException
    # 日本語コメント: TC2
    def detach_raise(ticket_id, label_id):
        raise MockDeskError("not found")
    service = MockLabelService(detach_behavior=detach_raise)
    with pytest.raises(HTTPException):
        call_detach_label(0, 1, service)

# --- TC3: 異常系 負のチケットID ---
def test_detach_label_TC3():
    # TC3: detachがDeskErrorを発生
    # ticket_id=-1
    # 期待される結果: HTTPException
    # 日本語コメント: TC3
    def detach_raise(ticket_id, label_id):
        raise MockDeskError("negative id")
    service = MockLabelService(detach_behavior=detach_raise)
    with pytest.raises(HTTPException):
        call_detach_label(-1, 1, service)

# --- TC4: 異常系 存在しないラベルID ---
def test_detach_label_TC4():
    # TC4: detachがDeskErrorを発生
    # label_id=0
    # 期待される結果: HTTPException
    # 日本語コメント: TC4
    def detach_raise(ticket_id, label_id):
        raise MockDeskError("not found label")
    service = MockLabelService(detach_behavior=detach_raise)
    with pytest.raises(HTTPException):
        call_detach_label(1, 0, service)

# --- TC5: 異常系 負のラベルID ---
def test_detach_label_TC5():
    # TC5: detachがDeskErrorを発生
    # label_id=-1
    # 期待される結果: HTTPException
    # 日本語コメント: TC5
    def detach_raise(ticket_id, label_id):
        raise MockDeskError("negative label id")
    service = MockLabelService(detach_behavior=detach_raise)
    with pytest.raises(HTTPException):
        call_detach_label(1, -1, service)

# --- TC6: 異常系 ticket_idがstr型 ---
def test_detach_label_TC6():
    # TC6: ticket_idがstr型
    # 期待される結果: TypeError
    # 日本語コメント: TC6
    service = MockLabelService(detach_behavior=MockTicketOut())
    with pytest.raises(TypeError):
        call_detach_label("a", 1, service)

# --- TC7: 異常系 label_idがstr型 ---
def test_detach_label_TC7():
    # TC7: label_idがstr型
    # 期待される結果: TypeError
    # 日本語コメント: TC7
    service = MockLabelService(detach_behavior=MockTicketOut())
    with pytest.raises(TypeError):
        call_detach_label(1, "b", service)

# --- TC8: 異常系 ticket_idがNone ---
def test_detach_label_TC8():
    # TC8: ticket_idがNone
    # 期待される結果: TypeError
    # 日本語コメント: TC8
    service = MockLabelService(detach_behavior=MockTicketOut())
    with pytest.raises(TypeError):
        call_detach_label(None, 1, service)

# --- TC9: 異常系 label_idがNone ---
def test_detach_label_TC9():
    # TC9: label_idがNone
    # 期待される結果: TypeError
    # 日本語コメント: TC9
    service = MockLabelService(detach_behavior=MockTicketOut())
    with pytest.raises(TypeError):
        call_detach_label(1, None, service)

# --- TC10: 異常系 serviceがNone ---
def test_detach_label_TC10():
    # TC10: serviceがNone
    # 期待される結果: AttributeError
    # 日本語コメント: TC10
    with pytest.raises(AttributeError):
        call_detach_label(1, 1, None)

# --- TC11: 異常系 detachでDeskError発生 ---
def test_detach_label_TC11():
    # TC11: detachがDeskErrorを投げるインスタンス
    # 期待される結果: HTTPException
    # 日本語コメント: TC11
    def detach_raise(ticket_id, label_id):
        raise MockDeskError("detach error")
    service = MockLabelService(detach_behavior=detach_raise)
    with pytest.raises(HTTPException):
        call_detach_label(1, 1, service)

# --- TC12: 異常系 detachでValueError発生 ---
def test_detach_label_TC12():
    # TC12: detachがValueErrorを投げるインスタンス
    # 期待される結果: ValueError
    # 日本語コメント: TC12
    def detach_raise(ticket_id, label_id):
        raise ValueError("unexpected error")
    service = MockLabelService(detach_behavior=detach_raise)
    with pytest.raises(ValueError):
        call_detach_label(1, 1, service)

# --- TC13: 異常系 detachがNoneを返す場合 ---
def test_detach_label_TC13():
    # TC13: detachがNoneを返すインスタンス
    # 期待される結果: TypeError
    # 日本語コメント: TC13
    service = MockLabelService(detach_behavior=None)
    with pytest.raises(TypeError):
        call_detach_label(1, 1, service)

# --- TC14: 異常系 detachがTicket以外の型を返す場合 ---
def test_detach_label_TC14():
    # TC14: detachがstrを返すインスタンス
    # 期待される結果: TypeError
    # 日本語コメント: TC14
    service = MockLabelService(detach_behavior="not a ticket")
    with pytest.raises(TypeError):
        call_detach_label(1, 1, service)