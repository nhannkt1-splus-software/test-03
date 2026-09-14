import pytest

# テスト対象関数・変数のimport
from target_module import is_valid_slug  # テスト対象のモジュール名に合わせて修正してください

# _SLUG_RE, slugifyの挙動に依存するため、ここでは関数の型・例外・代表的な挙動をテストします

# 正常系テスト
@pytest.mark.parametrize(
    "value, expected, case_id",
    [
        # TC1: すでに有効なスラッグ文字列
        ("valid-slug", True, "TC1"),
        # TC2: スペースを含む無効な文字列
        ("invalid slug", False, "TC2"),
        # TC3: アンダースコアと数字を含む有効な文字列
        ("valid_slug_123", True, "TC3"),
        # TC4: 空文字列
        ("", False, "TC4"),
        # TC5: 日本語文字列
        ("あいうえお", False, "TC5"),
        # TC6: 特殊文字を含む文字列
        ("slug-with-special-characters!@#", False, "TC6"),
        # TC7: 数字のみの文字列
        ("123", True, "TC7"),
        # TC8: 先頭と末尾にハイフンがある文字列
        ("-start-and-end-", False, "TC8"),
        # TC13: 1文字のスラッグ
        ("a", True, "TC13"),
        # TC14: 長いスラッグ
        ("a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z", True, "TC14"),
        # TC15: 先頭と末尾に連続したハイフンがある文字列
        ("--double-hyphen--", False, "TC15"),
        # TC16: 途中に連続したハイフンがある文字列
        ("a--b--c", True, "TC16"),
        # TC17: アンダースコアのみのスラッグ
        ("a_b_c", True, "TC17"),
        # TC18: 末尾にハイフンがある文字列
        ("a-b-c-", False, "TC18"),
        # TC19: 先頭にハイフンがある文字列
        ("-a-b-c", False, "TC19"),
        # TC20: スペースのみの文字列
        ("a b c", False, "TC20"),
    ]
)
def test_is_valid_slug_normal_cases(value, expected, case_id):
    # 各テストケースIDをコメントで明示
    # {case_id}
    assert is_valid_slug(value) == expected

# 型不一致（例外発生）テスト
@pytest.mark.parametrize(
    "value, case_id",
    [
        (None, "TC9"),   # None型
        (123, "TC10"),   # int型
        ([], "TC11"),    # list型
        ({}, "TC12"),    # dict型
    ]
)
def test_is_valid_slug_type_error(value, case_id):
    # {case_id}
    with pytest.raises(TypeError):
        is_valid_slug(value)