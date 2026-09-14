import pytest
from functools import partial

# --- テスト対象クラスのインポート ---
# from <your_module> import InvalidSlugError

# DeskErrorのダミー定義（テスト用、実際は本物をimportすること）
class DeskError(Exception):
    pass

# テスト対象クラスの再定義（実際はimportすること）
class InvalidSlugError(DeskError):
    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Invalid slug {slug}")

# --- テストケース ---

# TC1: 正常系：有効なスラッグ（英数字とアンダースコア）
def test_TC1_valid_slug():
    # テストID: TC1
    slug = "valid_slug"
    err = InvalidSlugError(slug)
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == f"Invalid slug {slug}"

# TC2: 正常系：空文字列（str型）
def test_TC2_empty_string_slug():
    # テストID: TC2
    slug = ""
    err = InvalidSlugError(slug)
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == "Invalid slug "

# TC3: 正常系：特殊文字を含むstr型
def test_TC3_special_characters_slug():
    # テストID: TC3
    slug = "slug-with-special-characters!@#"
    err = InvalidSlugError(slug)
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == f"Invalid slug {slug}"

# TC4: 正常系：1文字のスラッグ
def test_TC4_one_char_slug():
    # テストID: TC4
    slug = "a"
    err = InvalidSlugError(slug)
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == f"Invalid slug {slug}"

# TC5: 正常系：100文字の長いスラッグ
def test_TC5_long_slug():
    # テストID: TC5
    slug = "a" * 100
    err = InvalidSlugError(slug)
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == f"Invalid slug {slug}"

# TC6: 異常系：int型（型不一致）
def test_TC6_int_slug():
    # テストID: TC6
    slug = 123
    with pytest.raises(TypeError):
        InvalidSlugError(slug)

# TC7: 異常系：None型（型不一致）
def test_TC7_none_slug():
    # テストID: TC7
    slug = None
    with pytest.raises(TypeError):
        InvalidSlugError(slug)

# TC8: 異常系：list型（型不一致）
def test_TC8_list_slug():
    # テストID: TC8
    slug = ["slug"]
    with pytest.raises(TypeError):
        InvalidSlugError(slug)

# TC9: 異常系：dict型（型不一致）
def test_TC9_dict_slug():
    # テストID: TC9
    slug = {"slug": "value"}
    with pytest.raises(TypeError):
        InvalidSlugError(slug)

# TC10: 正常系：partial applicationで有効なスラッグを固定
def test_TC10_partial_valid_slug():
    # テストID: TC10
    slug = "valid_slug"
    partial_func = partial(InvalidSlugError, slug)
    err = partial_func()
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == f"Invalid slug {slug}"

# TC11: 正常系：partial applicationで空文字列slugを固定
def test_TC11_partial_empty_string_slug():
    # テストID: TC11
    slug = ""
    partial_func = partial(InvalidSlugError, slug)
    err = partial_func()
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == "Invalid slug "

# TC12: 正常系：partial applicationで特殊文字slugを固定
def test_TC12_partial_special_characters_slug():
    # テストID: TC12
    slug = "slug-with-special-characters!@#"
    partial_func = partial(InvalidSlugError, slug)
    err = partial_func()
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == f"Invalid slug {slug}"

# TC13: 正常系：partial applicationで1文字slugを固定
def test_TC13_partial_one_char_slug():
    # テストID: TC13
    slug = "a"
    partial_func = partial(InvalidSlugError, slug)
    err = partial_func()
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == f"Invalid slug {slug}"

# TC14: 正常系：partial applicationで100文字slugを固定
def test_TC14_partial_long_slug():
    # テストID: TC14
    slug = "a" * 100
    partial_func = partial(InvalidSlugError, slug)
    err = partial_func()
    assert err.slug == slug
    assert isinstance(err, InvalidSlugError)
    assert str(err) == f"Invalid slug {slug}"

# TC15: 異常系：partial applicationでint型slug（型不一致）
def test_TC15_partial_int_slug():
    # テストID: TC15
    slug = 123
    with pytest.raises(TypeError):
        partial_func = partial(InvalidSlugError, slug)
        partial_func()

# TC16: 異常系：partial applicationでNone型slug（型不一致）
def test_TC16_partial_none_slug():
    # テストID: TC16
    slug = None
    with pytest.raises(TypeError):
        partial_func = partial(InvalidSlugError, slug)
        partial_func()

# TC17: 異常系：partial applicationでlist型slug（型不一致）
def test_TC17_partial_list_slug():
    # テストID: TC17
    slug = ["slug"]
    with pytest.raises(TypeError):
        partial_func = partial(InvalidSlugError, slug)
        partial_func()

# TC18: 異常系：partial applicationでdict型slug（型不一致）
def test_TC18_partial_dict_slug():
    # テストID: TC18
    slug = {"slug": "value"}
    with pytest.raises(TypeError):
        partial_func = partial(InvalidSlugError, slug)
        partial_func()
```
