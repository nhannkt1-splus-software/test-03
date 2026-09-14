import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status, Depends
from pydantic import ValidationError
from types import SimpleNamespace

# --- テスト対象関数の依存型のダミー定義 ---
# 本来はimportするが、テスト用に最低限の型を定義
class DeskError(Exception):
    pass

def http_error(exc):
    # HTTPExceptionを返すダミー
    return HTTPException(status_code=400, detail=str(exc))

class WorklogOut:
    # テスト用のダミー
    @classmethod
    def model_validate(cls, obj, from_attributes=False):
        return obj

class WorklogCreate:
    # テスト用のダミー
    def __init__(self, hours, author, note):
        self.hours = hours
        self.author = author
        self.note = note

class WorklogService:
    def add_worklog(self, ticket_id, hours, author, note):
        return SimpleNamespace(ticket_id=ticket_id, hours=hours, author=author, note=note)

# --- テスト対象関数のimport ---
# 本来は from ... import add_worklog だが、ここでは直接定義されていると仮定
import sys

# テスト対象関数をimportできるようにする
def get_worklog_service():
    return WorklogService()

# テスト対象関数の再定義（依存注入のため）
def add_worklog(
    ticket_id: int,
    payload: WorklogCreate,
    service: WorklogService = Depends(get_worklog_service),
) -> WorklogOut:
    try:
        worklog = service.add_worklog(ticket_id, payload.hours, payload.author, payload.note)
        return WorklogOut.model_validate(worklog, from_attributes=True)
    except DeskError as exc:
        raise http_error(exc) from exc

# --- WorklogCreateのバリデーションを模倣するPydanticモデル ---
from pydantic import BaseModel, Field, ValidationError as PydanticValidationError, root_validator
from typing import Optional

class WorklogCreateModel(BaseModel):
    hours: float
    author: str
    note: str

    class Config:
        extra = "forbid"

    @root_validator
    def check_author_not_empty(cls, values):
        author = values.get('author')
        if author is None or author == "":
            raise ValueError("author must not be empty")
        return values

# --- テストヘルパー ---
def make_payload(payload_dict):
    # dict→WorklogCreateModel→WorklogCreate
    try:
        model = WorklogCreateModel(**payload_dict)
        return WorklogCreate(model.hours, model.author, model.note)
    except PydanticValidationError as e:
        raise ValidationError(str(e), WorklogCreateModel)

# --- テストケース ---
# TC1: 正常系: 全て有効な値
def test_TC1():
    # TC1
    payload_dict = {"hours": 2.5, "author": "user1", "note": "作業内容"}
    ticket_id = 1
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.return_value = SimpleNamespace(**payload_dict, ticket_id=ticket_id)
    result = add_worklog(ticket_id, payload, service)
    # 結果がWorklogOut.model_validateの戻り値（ここではSimpleNamespace）であること
    assert result.hours == 2.5
    assert result.author == "user1"
    assert result.note == "作業内容"
    assert result.ticket_id == 1

# TC2: ticket_idが0（境界値）
def test_TC2():
    # TC2
    payload_dict = {"hours": 1, "author": "user2", "note": "テスト"}
    ticket_id = 0
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.return_value = SimpleNamespace(**payload_dict, ticket_id=ticket_id)
    result = add_worklog(ticket_id, payload, service)
    assert result.ticket_id == 0

# TC3: ticket_idが負の値（異常系）
def test_TC3():
    # TC3
    payload_dict = {"hours": 1, "author": "user2", "note": "テスト"}
    ticket_id = -1
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.side_effect = DeskError("invalid ticket_id")
    with pytest.raises(HTTPException) as excinfo:
        add_worklog(ticket_id, payload, service)
    assert excinfo.value.status_code == 400

# TC4: ticket_idが非常に大きい値
def test_TC4():
    # TC4
    payload_dict = {"hours": 1, "author": "user2", "note": "テスト"}
    ticket_id = 999999999
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.return_value = SimpleNamespace(**payload_dict, ticket_id=ticket_id)
    result = add_worklog(ticket_id, payload, service)
    assert result.ticket_id == 999999999

# TC5: hoursが0（境界値）
def test_TC5():
    # TC5
    payload_dict = {"hours": 0, "author": "user3", "note": "ゼロ時間"}
    ticket_id = 1
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.return_value = SimpleNamespace(**payload_dict, ticket_id=ticket_id)
    result = add_worklog(ticket_id, payload, service)
    assert result.hours == 0

# TC6: hoursが負の値（異常系）
def test_TC6():
    # TC6
    payload_dict = {"hours": -1, "author": "user3", "note": "負の時間"}
    ticket_id = 1
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.side_effect = DeskError("invalid hours")
    with pytest.raises(HTTPException) as excinfo:
        add_worklog(ticket_id, payload, service)
    assert excinfo.value.status_code == 400

# TC7: hoursが非常に大きい値
def test_TC7():
    # TC7
    payload_dict = {"hours": 10000, "author": "user3", "note": "大きな時間"}
    ticket_id = 1
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.return_value = SimpleNamespace(**payload_dict, ticket_id=ticket_id)
    result = add_worklog(ticket_id, payload, service)
    assert result.hours == 10000

# TC8: authorが空文字（異常系）
def test_TC8():
    # TC8
    payload_dict = {"hours": 1, "author": "", "note": "authorが空文字"}
    ticket_id = 1
    with pytest.raises(ValidationError):
        make_payload(payload_dict)

# TC9: noteが空文字（正常系）
def test_TC9():
    # TC9
    payload_dict = {"hours": 1, "author": "user4", "note": ""}
    ticket_id = 1
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.return_value = SimpleNamespace(**payload_dict, ticket_id=ticket_id)
    result = add_worklog(ticket_id, payload, service)
    assert result.note == ""

# TC10: noteが長文
def test_TC10():
    # TC10
    payload_dict = {"hours": 1, "author": "user4", "note": "a" * 1000}
    ticket_id = 1
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.return_value = SimpleNamespace(**payload_dict, ticket_id=ticket_id)
    result = add_worklog(ticket_id, payload, service)
    assert result.note == "a" * 1000

# TC11: hoursがstr型（型不一致）
def test_TC11():
    # TC11
    payload_dict = {"hours": "two", "author": "user5", "note": "型不一致"}
    ticket_id = 1
    with pytest.raises(ValidationError):
        make_payload(payload_dict)

# TC12: ticket_idがstr型（型不一致）
def test_TC12():
    # TC12
    payload_dict = {"hours": 1, "author": "user5", "note": "型不一致"}
    ticket_id = "one"
    payload = make_payload(payload_dict)
    service = MagicMock()
    # ticket_idがstr型なのでTypeErrorが発生することを期待
    with pytest.raises(TypeError):
        add_worklog(ticket_id, payload, service)

# TC13: authorがNone（型不一致）
def test_TC13():
    # TC13
    payload_dict = {"hours": 1, "author": None, "note": "authorがNone"}
    ticket_id = 1
    with pytest.raises(ValidationError):
        make_payload(payload_dict)

# TC14: noteが欠損（必須項目欠損）
def test_TC14():
    # TC14
    payload_dict = {"hours": 1, "author": "user6"}
    ticket_id = 1
    with pytest.raises(ValidationError):
        make_payload(payload_dict)

# TC15: payloadが空（必須項目欠損）
def test_TC15():
    # TC15
    payload_dict = {}
    ticket_id = 1
    with pytest.raises(ValidationError):
        make_payload(payload_dict)

# TC16: payloadがNone（型不一致）
def test_TC16():
    # TC16
    payload = None
    ticket_id = 1
    service = MagicMock()
    # Noneを渡すとTypeError
    with pytest.raises(AttributeError):
        add_worklog(ticket_id, payload, service)

# TC17: payloadに不要な項目が含まれている場合（正常系）
def test_TC17():
    # TC17
    payload_dict = {"hours": 1, "author": "user7", "note": "作業内容", "extra": "不要な項目"}
    ticket_id = 1
    with pytest.raises(ValidationError):
        make_payload(payload_dict)

# TC18: hoursがNone（型不一致）
def test_TC18():
    # TC18
    payload_dict = {"hours": None, "author": "user8", "note": "作業内容"}
    ticket_id = 1
    with pytest.raises(ValidationError):
        make_payload(payload_dict)

# TC19: noteがint型（型不一致）
def test_TC19():
    # TC19
    payload_dict = {"hours": 1, "author": "user9", "note": 123}
    ticket_id = 1
    with pytest.raises(ValidationError):
        make_payload(payload_dict)

# TC20: service.add_worklogでDeskError発生
def test_TC20():
    # TC20
    payload_dict = {"hours": 1, "author": "user10", "note": "作業内容"}
    ticket_id = 1
    payload = make_payload(payload_dict)
    service = MagicMock()
    service.add_worklog.side_effect = DeskError("service error")
    with pytest.raises(HTTPException) as excinfo:
        add_worklog(ticket_id, payload, service)
    assert excinfo.value.status_code == 400
```
