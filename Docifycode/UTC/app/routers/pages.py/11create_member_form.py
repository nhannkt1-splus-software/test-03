import pytest
from unittest.mock import MagicMock, patch
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

# --- テスト用のダミークラス・例外定義 ---

class DeskError(Exception):
    pass

# テンプレート用のダミー
templates = Jinja2Templates(directory=".")

# --- テスト対象関数のimport ---
# create_member_form, get_member_serviceはグローバルスコープにあるものとする
from types import SimpleNamespace

# --- テスト用ヘルパー ---

@pytest.fixture
def dummy_request():
    # RequestはFastAPI/StarletteのRequest型
    # 実際のRequestオブジェクトは複雑なので、必要な属性だけ持つダミーを使う
    return MagicMock(spec=Request)

@pytest.fixture
def dummy_templates(monkeypatch):
    # テンプレートのTemplateResponseをモック
    monkeypatch.setattr("templates", templates)

# --- テストケース ---

# TC1: 正常系：有効なユーザー名と表示名でメンバー作成
def test_TC1_create_member_success(dummy_request):
    # テストID: TC1
    member_service = MagicMock()
    member_service.create_member.return_value = None
    # list_membersは呼ばれない
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username="valid_username",
        display_name="valid_display_name",
        members=member_service,
    )
    # リダイレクトレスポンスであること
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == "/members"

# TC2: 異常系：ユーザー名が空文字列の場合
def test_TC2_create_member_username_empty_raises_deskerror(dummy_request):
    # テストID: TC2
    member_service = MagicMock()
    member_service.create_member.side_effect = DeskError("ユーザー名が空です")
    member_service.list_members.return_value = []
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username="",
        display_name="valid_display_name",
        members=member_service,
    )
    # TemplateResponseが返ること
    assert hasattr(response, "template")
    assert response.status_code == 400
    assert "error" in response.context
    assert "ユーザー名が空" in response.context["error"]

# TC3: 異常系：表示名が空文字列の場合
def test_TC3_create_member_display_name_empty_raises_deskerror(dummy_request):
    # テストID: TC3
    member_service = MagicMock()
    member_service.create_member.side_effect = DeskError("表示名が空です")
    member_service.list_members.return_value = []
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username="valid_username",
        display_name="",
        members=member_service,
    )
    assert hasattr(response, "template")
    assert response.status_code == 400
    assert "error" in response.context
    assert "表示名が空" in response.context["error"]

# TC4: 正常系：特殊文字を含むユーザー名・表示名
def test_TC4_create_member_special_chars(dummy_request):
    # テストID: TC4
    member_service = MagicMock()
    member_service.create_member.return_value = None
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username="user_with_special_chars!@#",
        display_name="display_with_special_chars!@#",
        members=member_service,
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == "/members"

# TC5: 異常系：usernameがNoneの場合（型不正）
def test_TC5_create_member_username_none_typeerror(dummy_request):
    # テストID: TC5
    member_service = MagicMock()
    from target import create_member_form
    with pytest.raises(TypeError):
        create_member_form(
            request=dummy_request,
            username=None,
            display_name="valid_display_name",
            members=member_service,
        )

# TC6: 異常系：display_nameがNoneの場合（型不正）
def test_TC6_create_member_display_name_none_typeerror(dummy_request):
    # テストID: TC6
    member_service = MagicMock()
    from target import create_member_form
    with pytest.raises(TypeError):
        create_member_form(
            request=dummy_request,
            username="valid_username",
            display_name=None,
            members=member_service,
        )

# TC7: 異常系：usernameが整数型の場合（型不正）
def test_TC7_create_member_username_int_typeerror(dummy_request):
    # テストID: TC7
    member_service = MagicMock()
    from target import create_member_form
    with pytest.raises(TypeError):
        create_member_form(
            request=dummy_request,
            username=123,
            display_name="valid_display_name",
            members=member_service,
        )

# TC8: 異常系：display_nameがfloat型の場合（型不正）
def test_TC8_create_member_display_name_float_typeerror(dummy_request):
    # テストID: TC8
    member_service = MagicMock()
    from target import create_member_form
    with pytest.raises(TypeError):
        create_member_form(
            request=dummy_request,
            username="valid_username",
            display_name=123.45,
            members=member_service,
        )

# TC9: 異常系：usernameがリスト型の場合（型不正）
def test_TC9_create_member_username_list_typeerror(dummy_request):
    # テストID: TC9
    member_service = MagicMock()
    from target import create_member_form
    with pytest.raises(TypeError):
        create_member_form(
            request=dummy_request,
            username=[],
            display_name="valid_display_name",
            members=member_service,
        )

# TC10: 異常系：display_nameが辞書型の場合（型不正）
def test_TC10_create_member_display_name_dict_typeerror(dummy_request):
    # テストID: TC10
    member_service = MagicMock()
    from target import create_member_form
    with pytest.raises(TypeError):
        create_member_form(
            request=dummy_request,
            username="valid_username",
            display_name={},
            members=member_service,
        )

# TC11: 正常系：100文字の長いユーザー名・表示名
def test_TC11_create_member_long_username_display_name(dummy_request):
    # テストID: TC11
    member_service = MagicMock()
    member_service.create_member.return_value = None
    long_username = "a" * 100
    long_display_name = "b" * 100
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username=long_username,
        display_name=long_display_name,
        members=member_service,
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == "/members"

# TC12: 異常系：ユーザー名が半角スペースのみの場合
def test_TC12_create_member_username_space_raises_deskerror(dummy_request):
    # テストID: TC12
    member_service = MagicMock()
    member_service.create_member.side_effect = DeskError("ユーザー名が不正です")
    member_service.list_members.return_value = []
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username=" ",
        display_name="valid_display_name",
        members=member_service,
    )
    assert hasattr(response, "template")
    assert response.status_code == 400
    assert "error" in response.context
    assert "ユーザー名が不正" in response.context["error"]

# TC13: 異常系：表示名が半角スペースのみの場合
def test_TC13_create_member_display_name_space_raises_deskerror(dummy_request):
    # テストID: TC13
    member_service = MagicMock()
    member_service.create_member.side_effect = DeskError("表示名が不正です")
    member_service.list_members.return_value = []
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username="valid_username",
        display_name=" ",
        members=member_service,
    )
    assert hasattr(response, "template")
    assert response.status_code == 400
    assert "error" in response.context
    assert "表示名が不正" in response.context["error"]

# TC14: 正常系：メンバー一覧が空の場合の新規作成
def test_TC14_create_member_list_members_empty(dummy_request):
    # テストID: TC14
    member_service = MagicMock()
    member_service.create_member.return_value = None
    member_service.list_members.return_value = []
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username="valid_username",
        display_name="valid_display_name",
        members=member_service,
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == "/members"

# TC15: 正常系：メンバー一覧が大量の場合の新規作成
def test_TC15_create_member_list_members_many(dummy_request):
    # テストID: TC15
    member_service = MagicMock()
    member_service.create_member.return_value = None
    member_service.list_members.return_value = [{"username": f"user{i}"} for i in range(1000)]
    from target import create_member_form
    response = create_member_form(
        request=dummy_request,
        username="valid_username",
        display_name="valid_display_name",
        members=member_service,
    )
    assert isinstance(response, RedirectResponse)
    assert response.status_code == 303
    assert response.headers["location"] == "/members"

# TC16: 異常系：create_memberで予期しない例外（TypeError）が発生した場合
def test_TC16_create_member_unexpected_typeerror(dummy_request):
    # テストID: TC16
    member_service = MagicMock()
    member_service.create_member.side_effect = TypeError("予期しない型エラー")
    from target import create_member_form
    with pytest.raises(TypeError):
        create_member_form(
            request=dummy_request,
            username="valid_username",
            display_name="valid_display_name",
            members=member_service,
        )
```
