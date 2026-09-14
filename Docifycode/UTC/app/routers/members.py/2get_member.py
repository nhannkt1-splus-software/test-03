import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from pydantic import ValidationError

# テスト対象のFastAPIアプリをインポート
from your_module import app, router, MemberService, MemberOut, DeskError, http_error

client = TestClient(app)

# --- TC1: 正常系：存在する会員IDを指定した場合 ---
def test_get_member_tc1():
    # TC1
    member_id = 1
    expected_member = {"id": member_id, "name": "テスト会員"}
    # MemberService.get_memberをモック
    with patch("your_module.get_member_service") as mock_dep:
        mock_service = MagicMock()
        mock_service.get_member.return_value = expected_member
        mock_dep.return_value = mock_service
        # API呼び出し
        response = client.get(f"/{member_id}")
        # レスポンス検証
        assert response.status_code == 200  # 正常系
        assert response.json()["id"] == member_id
        assert response.json()["name"] == "テスト会員"

# --- TC2: 異常系：存在しない会員IDを指定した場合 ---
def test_get_member_tc2():
    # TC2
    member_id = 999999
    with patch("your_module.get_member_service") as mock_dep:
        mock_service = MagicMock()
        mock_service.get_member.side_effect = DeskError("not found")
        mock_dep.return_value = mock_service
        response = client.get(f"/{member_id}")
        # DeskErrorがhttp_errorで変換されることを検証
        assert response.status_code == 400 or response.status_code == 404

# --- TC3: 境界値：0のmember_idを指定した場合 ---
def test_get_member_tc3():
    # TC3
    member_id = 0
    with patch("your_module.get_member_service") as mock_dep:
        mock_service = MagicMock()
        mock_service.get_member.side_effect = DeskError("invalid id")
        mock_dep.return_value = mock_service
        response = client.get(f"/{member_id}")
        assert response.status_code == 400 or response.status_code == 404

# --- TC4: 異常系：負のmember_idを指定した場合 ---
def test_get_member_tc4():
    # TC4
    member_id = -1
    with patch("your_module.get_member_service") as mock_dep:
        mock_service = MagicMock()
        mock_service.get_member.side_effect = DeskError("invalid id")
        mock_dep.return_value = mock_service
        response = client.get(f"/{member_id}")
        assert response.status_code == 400 or response.status_code == 404

# --- TC5: 異常系：member_idがstr型の場合 ---
def test_get_member_tc5():
    # TC5
    member_id = "abc"
    response = client.get(f"/{member_id}")
    # FastAPI/Pydanticによる型エラー
    assert response.status_code == 422  # Unprocessable Entity

# --- TC6: 異常系：member_idがNoneの場合 ---
def test_get_member_tc6():
    # TC6
    member_id = None
    response = client.get(f"/{member_id}")
    # FastAPI/Pydanticによる型エラー
    assert response.status_code == 404  # パスパラメータがNoneの場合は404

# --- TC7: 異常系：member_idがfloat型の場合 ---
def test_get_member_tc7():
    # TC7
    member_id = 1.5
    response = client.get(f"/{member_id}")
    # FastAPI/Pydanticによる型エラー
    assert response.status_code == 422  # Unprocessable Entity

# --- TC8: 異常系：MemberOut.model_validateでバリデーションエラーが発生する場合 ---
def test_get_member_tc8():
    # TC8
    member_id = 1
    invalid_member = {"id": member_id, "name": None}  # nameがNoneでバリデーションエラー
    with patch("your_module.get_member_service") as mock_dep:
        mock_service = MagicMock()
        mock_service.get_member.return_value = invalid_member
        mock_dep.return_value = mock_service
        response = client.get(f"/{member_id}")
        # MemberOut.model_validateでValidationErrorが発生し、FastAPIは422を返す
        assert response.status_code == 422