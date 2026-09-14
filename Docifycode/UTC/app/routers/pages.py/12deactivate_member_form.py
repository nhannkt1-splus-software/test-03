import pytest
from unittest.mock import MagicMock, patch
from fastapi import Request
from fastapi.responses import RedirectResponse

# --- テスト用のダミークラス・例外定義 ---

# DeskError例外のダミー定義
class DeskError(Exception):
    pass

# templates.TemplateResponseのダミー
class DummyTemplateResponse:
    def __init__(self, request, template_name, context, status_code=None):
        self.request = request
        self.template_name = template_name
        self.context = context
        self.status_code = status_code

# --- テスト対象関数のimport ---
# deactivate_member_form, get_member_service, templatesはグローバルスコープでimportされている前提

# --- テストケース ---

# TC1: 正常系：存在する会員IDで退会処理が成功するケース
def test_TC1_deactivate_member_success(monkeypatch):
    # テストID: TC1
    # --- モックの準備 ---
    mock_members = MagicMock()
    mock_members.deactivate.return_value = None
    mock_request = MagicMock(spec=Request)
    # templates.TemplateResponseは使われないのでpatch不要

    # --- テスト実行 ---
    with patch("your_module_name.get_member_service", return_value=mock_members):
        from your_module_name import deactivate_member_form
        response = deactivate_member_form(
            member_id=1,
            request=mock_request,
            members=mock_members
        )

    # --- 検証 ---
    # 正常時はRedirectResponseが返る
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == "/members"

# TC2: 異常系：存在しない会員IDで退会処理が失敗し、DeskErrorが発生するケース
def test_TC2_deactivate_member_deskerror(monkeypatch):
    # テストID: TC2
    mock_members = MagicMock()
    mock_members.deactivate.side_effect = DeskError("not found")
    mock_members.list_members.return_value = ["dummy_member"]
    mock_request = MagicMock(spec=Request)

    # templates.TemplateResponseをダミーに差し替え
    with patch("your_module_name.templates.TemplateResponse", DummyTemplateResponse):
        from your_module_name import deactivate_member_form
        response = deactivate_member_form(
            member_id=99999,
            request=mock_request,
            members=mock_members
        )

    # DeskError時はTemplateResponseが返る
    assert isinstance(response, DummyTemplateResponse)
    assert response.template_name == "members.html"
    assert response.context["error"] == "not found"
    assert response.status_code == 409

# TC3: 境界値テスト：member_idが0の場合、DeskErrorが発生するケース
def test_TC3_deactivate_member_id_zero(monkeypatch):
    # テストID: TC3
    mock_members = MagicMock()
    mock_members.deactivate.side_effect = DeskError("invalid id")
    mock_members.list_members.return_value = []
    mock_request = MagicMock(spec=Request)

    with patch("your_module_name.templates.TemplateResponse", DummyTemplateResponse):
        from your_module_name import deactivate_member_form
        response = deactivate_member_form(
            member_id=0,
            request=mock_request,
            members=mock_members
        )

    assert isinstance(response, DummyTemplateResponse)
    assert response.context["error"] == "invalid id"
    assert response.status_code == 409

# TC4: 異常系：member_idが負の値の場合、DeskErrorが発生するケース
def test_TC4_deactivate_member_id_negative(monkeypatch):
    # テストID: TC4
    mock_members = MagicMock()
    mock_members.deactivate.side_effect = DeskError("invalid id")
    mock_members.list_members.return_value = []
    mock_request = MagicMock(spec=Request)

    with patch("your_module_name.templates.TemplateResponse", DummyTemplateResponse):
        from your_module_name import deactivate_member_form
        response = deactivate_member_form(
            member_id=-1,
            request=mock_request,
            members=mock_members
        )

    assert isinstance(response, DummyTemplateResponse)
    assert response.context["error"] == "invalid id"
    assert response.status_code == 409

# TC5: 異常系：member_idが文字列の場合、TypeErrorが発生するケース
def test_TC5_deactivate_member_id_str(monkeypatch):
    # テストID: TC5
    mock_members = MagicMock()
    mock_request = MagicMock(spec=Request)

    from your_module_name import deactivate_member_form
    with pytest.raises(TypeError):
        deactivate_member_form(
            member_id="abc",  # 型不一致
            request=mock_request,
            members=mock_members
        )

# TC6: 異常系：member_idがnull（NoneType）の場合、TypeErrorが発生するケース
def test_TC6_deactivate_member_id_none(monkeypatch):
    # テストID: TC6
    mock_members = MagicMock()
    mock_request = MagicMock(spec=Request)

    from your_module_name import deactivate_member_form
    with pytest.raises(TypeError):
        deactivate_member_form(
            member_id=None,  # NoneType
            request=mock_request,
            members=mock_members
        )

# TC7: 異常系：member_idがint型の最大値の場合、存在しないIDとしてDeskErrorが発生するケース
def test_TC7_deactivate_member_id_max(monkeypatch):
    # テストID: TC7
    mock_members = MagicMock()
    mock_members.deactivate.side_effect = DeskError("not found")
    mock_members.list_members.return_value = []
    mock_request = MagicMock(spec=Request)

    with patch("your_module_name.templates.TemplateResponse", DummyTemplateResponse):
        from your_module_name import deactivate_member_form
        response = deactivate_member_form(
            member_id=2147483647,
            request=mock_request,
            members=mock_members
        )

    assert isinstance(response, DummyTemplateResponse)
    assert response.context["error"] == "not found"
    assert response.status_code == 409

# TC8: 異常系：member_idがint型の最小値の場合、無効なIDとしてDeskErrorが発生するケース
def test_TC8_deactivate_member_id_min(monkeypatch):
    # テストID: TC8
    mock_members = MagicMock()
    mock_members.deactivate.side_effect = DeskError("invalid id")
    mock_members.list_members.return_value = []
    mock_request = MagicMock(spec=Request)

    with patch("your_module_name.templates.TemplateResponse", DummyTemplateResponse):
        from your_module_name import deactivate_member_form
        response = deactivate_member_form(
            member_id=-2147483648,
            request=mock_request,
            members=mock_members
        )

    assert isinstance(response, DummyTemplateResponse)
    assert response.context["error"] == "invalid id"
    assert response.status_code == 409
```
