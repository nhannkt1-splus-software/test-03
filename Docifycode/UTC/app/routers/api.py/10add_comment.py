import pytest
from fastapi import HTTPException, status
from pydantic import ValidationError
from unittest.mock import Mock
from types import SimpleNamespace

# テスト対象関数と依存クラスのインポート
# 必要に応じてパスを調整してください
from your_module import add_comment, CommentCreate, CommentOut, DeskError, http_error

# TicketServiceのモック作成
class MockTicketService:
    def __init__(self, raise_error=None, return_value=None):
        self.raise_error = raise_error
        self.return_value = return_value

    def add_comment(self, ticket_id, body, author):
        if self.raise_error:
            raise self.raise_error
        return self.return_value or {
            "id": 123,
            "ticket_id": ticket_id,
            "body": body,
            "author": author,
        }

# get_ticket_serviceのモック
def get_ticket_service_mock(service):
    return service

# テストケースTC1: 正常系（全ての入力が正しい場合）
def test_add_comment_TC1():
    # TC1
    payload = CommentCreate(body="有効なコメント本文", author="user1")
    ticket_id = 1
    service = MockTicketService()
    result = add_comment(ticket_id, payload, service)
    assert isinstance(result, CommentOut)
    assert result.body == "有効なコメント本文"
    assert result.author == "user1"
    assert result.ticket_id == 1

# テストケースTC2: ticket_idが0（存在しないチケットID）
def test_add_comment_TC2():
    # TC2
    payload = CommentCreate(body="有効なコメント本文", author="user1")
    ticket_id = 0
    service = MockTicketService(raise_error=DeskError("not found"))
    with pytest.raises(HTTPException):
        add_comment(ticket_id, payload, service)

# テストケースTC3: ticket_idが負の値
def test_add_comment_TC3():
    # TC3
    payload = CommentCreate(body="有効なコメント本文", author="user1")
    ticket_id = -1
    service = MockTicketService(raise_error=DeskError("invalid id"))
    with pytest.raises(HTTPException):
        add_comment(ticket_id, payload, service)

# テストケースTC4: ticket_idが文字列（型不一致）
def test_add_comment_TC4():
    # TC4
    payload = CommentCreate(body="有効なコメント本文", author="user1")
    ticket_id = "abc"
    service = MockTicketService()
    with pytest.raises(TypeError):
        add_comment(ticket_id, payload, service)

# テストケースTC5: ticket_idがNone（型不一致）
def test_add_comment_TC5():
    # TC5
    payload = CommentCreate(body="有効なコメント本文", author="user1")
    ticket_id = None
    service = MockTicketService()
    with pytest.raises(TypeError):
        add_comment(ticket_id, payload, service)

# テストケースTC6: bodyが空文字列
def test_add_comment_TC6():
    # TC6
    payload = CommentCreate(body="", author="user1")
    ticket_id = 1
    service = MockTicketService(raise_error=DeskError("empty body"))
    with pytest.raises(HTTPException):
        add_comment(ticket_id, payload, service)

# テストケースTC7: authorが空文字列
def test_add_comment_TC7():
    # TC7
    payload = CommentCreate(body="有効なコメント本文", author="")
    ticket_id = 1
    service = MockTicketService(raise_error=DeskError("empty author"))
    with pytest.raises(HTTPException):
        add_comment(ticket_id, payload, service)

# テストケースTC8: bodyが非常に長い文字列
def test_add_comment_TC8():
    # TC8
    long_body = "a" * 10000
    payload = CommentCreate(body=long_body, author="user1")
    ticket_id = 1
    service = MockTicketService()
    result = add_comment(ticket_id, payload, service)
    assert isinstance(result, CommentOut)
    assert result.body == long_body
    assert result.author == "user1"
    assert result.ticket_id == 1

# テストケースTC9: authorが欠落
def test_add_comment_TC9():
    # TC9
    payload_dict = {"body": "有効なコメント本文"}
    ticket_id = 1
    service = MockTicketService()
    with pytest.raises(ValidationError):
        payload = CommentCreate(**payload_dict)
        add_comment(ticket_id, payload, service)

# テストケースTC10: bodyが欠落
def test_add_comment_TC10():
    # TC10
    payload_dict = {"author": "user1"}
    ticket_id = 1
    service = MockTicketService()
    with pytest.raises(ValidationError):
        payload = CommentCreate(**payload_dict)
        add_comment(ticket_id, payload, service)

# テストケースTC11: payloadがNone（型不一致）
def test_add_comment_TC11():
    # TC11
    payload = None
    ticket_id = 1
    service = MockTicketService()
    with pytest.raises(ValidationError):
        # Pydanticの型バリデーションを模倣
        CommentCreate.model_validate(payload)
        add_comment(ticket_id, payload, service)

# テストケースTC12: payloadが文字列（型不一致）
def test_add_comment_TC12():
    # TC12
    payload = "invalid_payload"
    ticket_id = 1
    service = MockTicketService()
    with pytest.raises(ValidationError):
        CommentCreate.model_validate(payload)
        add_comment(ticket_id, payload, service)

# テストケースTC13: bodyが非常に長く、authorが空文字列
def test_add_comment_TC13():
    # TC13
    long_body = "a" * 10000
    payload = CommentCreate(body=long_body, author="")
    ticket_id = 1
    service = MockTicketService(raise_error=DeskError("empty author"))
    with pytest.raises(HTTPException):
        add_comment(ticket_id, payload, service)

# テストケースTC14: bodyとauthorが両方空文字列
def test_add_comment_TC14():
    # TC14
    payload = CommentCreate(body="", author="")
    ticket_id = 1
    service = MockTicketService(raise_error=DeskError("empty body and author"))
    with pytest.raises(HTTPException):
        add_comment(ticket_id, payload, service)

# テストケースTC15: ticket_idが0かつbodyが空文字列
def test_add_comment_TC15():
    # TC15
    payload = CommentCreate(body="", author="user1")
    ticket_id = 0
    service = MockTicketService(raise_error=DeskError("not found and empty body"))
    with pytest.raises(HTTPException):
        add_comment(ticket_id, payload, service)

# テストケースTC16: ticket_idが負の値かつbodyが空文字列
def test_add_comment_TC16():
    # TC16
    payload = CommentCreate(body="", author="user1")
    ticket_id = -1
    service = MockTicketService(raise_error=DeskError("invalid id and empty body"))
    with pytest.raises(HTTPException):
        add_comment(ticket_id, payload, service)

# テストケースTC17: payloadに余分なフィールドが含まれている場合
def test_add_comment_TC17():
    # TC17
    payload_dict = {"body": "a" * 10000, "author": "user1", "extra": "unexpected"}
    ticket_id = 1
    service = MockTicketService()
    payload = CommentCreate.model_validate(payload_dict)
    result = add_comment(ticket_id, payload, service)
    assert isinstance(result, CommentOut)
    assert result.body == "a" * 10000
    assert result.author == "user1"
    assert result.ticket_id == 1
```
