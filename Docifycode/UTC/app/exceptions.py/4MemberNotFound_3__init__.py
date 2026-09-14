import pytest

# DeskErrorが未定義の場合、テスト用にダミークラスを定義
class DeskError(Exception):
    pass

from target_module import MemberNotFound  # 実際のテストでは適切なimportに置き換えてください

# 正常系テスト
@pytest.mark.parametrize(
    "test_id, key, expected_message",
    [
        # TC1: int型の正の値
        ("TC1", 1, "Member 1 was not found"),
        # TC2: int型のゼロ
        ("TC2", 0, "Member 0 was not found"),
        # TC3: int型の負の値
        ("TC3", -1, "Member -1 was not found"),
        # TC4: int型の非常に大きい値
        ("TC4", 999999999, "Member 999999999 was not found"),
        # TC5: str型の英数字文字列
        ("TC5", "user123", "Member user123 was not found"),
        # TC6: str型の空文字列
        ("TC6", "", "Member  was not found"),
        # TC7: str型の日本語文字列
        ("TC7", "あいうえお", "Member あいうえお was not found"),
        # TC8: str型の特殊文字列
        ("TC8", "!@#$%^&*()", "Member !@#$%^&*() was not found"),
        # TC13: str型の非常に長い文字列
        ("TC13", "a" * 100, f"Member {'a'*100} was not found"),
        # TC14: str型のスペースのみの文字列
        ("TC14", " ", "Member   was not found"),
    ]
)
def test_member_not_found_normal_cases(test_id, key, expected_message):
    # --- {test_id} 正常系テスト ---
    err = MemberNotFound(key)
    # key属性が正しくセットされているか確認
    assert err.key == key, f"{test_id}: key属性が正しくセットされていません"
    # エラーメッセージが正しいか確認
    assert str(err) == expected_message, f"{test_id}: エラーメッセージが正しくありません"

# 異常系テスト（型不一致）
@pytest.mark.parametrize(
    "test_id, key",
    [
        # TC9: None型（型不一致）
        ("TC9", None),
        # TC10: float型（型不一致）
        ("TC10", 3.14),
        # TC11: list型（型不一致）
        ("TC11", [1, 2, 3]),
        # TC12: dict型（型不一致）
        ("TC12", {"key": "value"}),
    ]
)
def test_member_not_found_type_error_cases(test_id, key):
    # --- {test_id} 異常系テスト（型不一致） ---
    with pytest.raises(TypeError):
        MemberNotFound(key)