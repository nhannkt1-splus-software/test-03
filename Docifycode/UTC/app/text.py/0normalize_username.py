import pytest

# テスト対象関数のインポート
from target import normalize_username

# 正常系テストケース
@pytest.mark.parametrize(
    "value, expected",
    [
        # TC1: 通常の英字文字列
        ("Alice", "alice"),  # TC1
        # TC2: 前後に空白がある文字列
        ("  Alice  ", "alice"),  # TC2
        # TC3: 大文字のみの文字列
        ("ALICE", "alice"),  # TC3
        # TC4: 小文字のみの文字列
        ("alice", "alice"),  # TC4
        # TC5: 大小混在の文字列
        ("AlIcE", "alice"),  # TC5
        # TC6: 日本語文字列
        ("アリス", "アリス"),  # TC6
        # TC7: 英字＋数字＋空白の文字列
        (" alice123 ", "alice123"),  # TC7
        # TC8: メールアドレス形式の文字列
        ("alice@domain.com", "alice@domain.com"),  # TC8
        # TC9: 空文字列
        ("", ""),  # TC9
        # TC10: 空白のみの文字列
        ("   ", ""),  # TC10
        # TC11: タブや改行を含む文字列
        ("\tAlice\n", "alice"),  # TC11
        # TC12: 1文字の文字列
        ("a", "a"),  # TC12
        # TC13: 100文字の長い文字列
        ("a" * 100, "a" * 100),  # TC13
        # TC19: 大文字＋数字の文字列
        ("ALICE123", "alice123"),  # TC19
        # TC20: 前後空白＋メールアドレス形式＋大小混在
        (" Alice@Domain.Com ", "alice@domain.com"),  # TC20
        # TC21: 全角英字の文字列
        ("ＡＬＩＣＥ", "ａｌｉｃｅ"),  # TC21
        # TC22: アンダースコアを含む文字列
        ("alice_123", "alice_123"),  # TC22
        # TC23: 空白2文字のみの文字列
        ("  ", ""),  # TC23
        # TC24: 改行とタブのみの文字列
        ("\n\t", ""),  # TC24
        # TC25: 記号を含む文字列
        ("Alice!", "alice!"),  # TC25
    ]
)
def test_normalize_username_normal(value, expected):
    # 各テストケースIDは上記コメント参照
    assert normalize_username(value) == expected

# 異常系テストケース（型不一致）
@pytest.mark.parametrize(
    "value, test_id",
    [
        (None, "TC14"),  # TC14: None型
        (123, "TC15"),   # TC15: int型
        (0.5, "TC16"),   # TC16: float型
        ([], "TC17"),    # TC17: list型
        ({}, "TC18"),    # TC18: dict型
    ]
)
def test_normalize_username_type_error(value, test_id):
    # 異常系：型不一致の場合はAttributeErrorが発生することを確認
    with pytest.raises(AttributeError):
        normalize_username(value)
```
