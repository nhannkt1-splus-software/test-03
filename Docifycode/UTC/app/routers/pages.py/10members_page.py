import pytest
from unittest.mock import Mock
from fastapi import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

# テスト対象関数のインポート
# from <your_module> import members_page

# テンプレートのモック
templates = Mock(spec=Jinja2Templates)
templates.TemplateResponse = Mock(return_value="template_response_mock")

# --- テストケース: TC1 正常系 ---
def test_members_page_tc1(monkeypatch):
    # TC1: 正常なMemberServiceインスタンスとRequestオブジェクト
    # メンバーサービスのモック
    member_service = Mock()
    member_service.list_members.return_value = [{"id": 1, "name": "Alice"}]
    # Requestオブジェクトのモック
    request = Mock(spec=Request)
    # templatesをパッチ
    monkeypatch.setattr("templates", templates)
    # テンプレートレスポンスの戻り値を確認
    result = members_page(request, member_service)
    assert result == "template_response_mock"
    templates.TemplateResponse.assert_called_once_with(
        request,
        "members.html",
        {"members": [{"id": 1, "name": "Alice"}], "error": None},
    )

# --- テストケース: TC2 正常系（空リスト） ---
def test_members_page_tc2(monkeypatch):
    # TC2: members.list_members()が空リストを返す場合
    member_service = Mock()
    member_service.list_members.return_value = []
    request = Mock(spec=Request)
    monkeypatch.setattr("templates", templates)
    result = members_page(request, member_service)
    assert result == "template_response_mock"
    templates.TemplateResponse.assert_called_once_with(
        request,
        "members.html",
        {"members": [], "error": None},
    )

# --- テストケース: TC3 異常系（requestがNone） ---
def test_members_page_tc3(monkeypatch):
    # TC3: requestがNoneの場合
    member_service = Mock()
    member_service.list_members.return_value = [{"id": 1}]
    monkeypatch.setattr("templates", templates)
    with pytest.raises(TypeError):
        members_page(None, member_service)

# --- テストケース: TC4 異常系（requestがint型） ---
def test_members_page_tc4(monkeypatch):
    # TC4: requestがint型の場合
    member_service = Mock()
    member_service.list_members.return_value = [{"id": 1}]
    monkeypatch.setattr("templates", templates)
    with pytest.raises(TypeError):
        members_page(1, member_service)

# --- テストケース: TC5 異常系（membersがNone） ---
def test_members_page_tc5(monkeypatch):
    # TC5: membersがNoneの場合
    request = Mock(spec=Request)
    monkeypatch.setattr("templates", templates)
    with pytest.raises(AttributeError):
        members_page(request, None)

# --- テストケース: TC6 異常系（membersがstr型） ---
def test_members_page_tc6(monkeypatch):
    # TC6: membersがstr型の場合
    request = Mock(spec=Request)
    monkeypatch.setattr("templates", templates)
    with pytest.raises(AttributeError):
        members_page(request, "invalid")

# --- テストケース: TC7 異常系（members.list_members()が例外を投げる） ---
def test_members_page_tc7(monkeypatch):
    # TC7: members.list_members()が例外を投げる場合
    member_service = Mock()
    member_service.list_members.side_effect = Exception("list_members error")
    request = Mock(spec=Request)
    monkeypatch.setattr("templates", templates)
    with pytest.raises(Exception):
        members_page(request, member_service)

# --- テストケース: TC8 異常系（members.list_members()がNoneを返す） ---
def test_members_page_tc8(monkeypatch):
    # TC8: members.list_members()がNoneを返す場合
    member_service = Mock()
    member_service.list_members.return_value = None
    request = Mock(spec=Request)
    monkeypatch.setattr("templates", templates)
    result = members_page(request, member_service)
    assert result == "template_response_mock"
    templates.TemplateResponse.assert_called_once_with(
        request,
        "members.html",
        {"members": None, "error": None},
    )

# --- テストケース: TC9 異常系（membersがlist_members()を持たないオブジェクト） ---
def test_members_page_tc9(monkeypatch):
    # TC9: membersがlist_members()を持たないオブジェクトの場合
    class Dummy:
        pass
    dummy_members = Dummy()
    request = Mock(spec=Request)
    monkeypatch.setattr("templates", templates)
    with pytest.raises(AttributeError):
        members_page(request, dummy_members)
```
