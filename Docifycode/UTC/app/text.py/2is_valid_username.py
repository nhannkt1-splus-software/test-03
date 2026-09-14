import pytest

# テスト対象関数と依存関数・変数をimport
from target_module import is_valid_username

# テストID: TC1
def test_TC1_valid_alphanumeric_username():
    # 正常系：英数字のみの有効なユーザー名
    assert is_valid_username("validUser123") is True

# テストID: TC2
def test_TC2_valid_username_with_underscore():
    # 正常系：アンダースコアを含む有効なユーザー名
    assert is_valid_username("user_name") is True

# テストID: TC3
def test_TC3_username_with_japanese_characters():
    # 正常系：日本語を含むユーザー名（正規表現が許容する場合）
    assert is_valid_username("ユーザー名") is True

# テストID: TC4
def test_TC4_username_with_period():
    # 正常系：ピリオドを含むユーザー名（許容される場合）
    assert is_valid_username("user.name") is True

# テストID: TC5
def test_TC5_username_with_hyphen():
    # 正常系：ハイフンを含むユーザー名（許容される場合）
    assert is_valid_username("user-name") is True

# テストID: TC6
def test_TC6_username_with_invalid_symbol_at():
    # 異常系：許可されていない記号（@）を含むユーザー名
    assert is_valid_username("user@name") is False

# テストID: TC7
def test_TC7_empty_string():
    # 異常系：空文字列
    assert is_valid_username("") is False

# テストID: TC8
def test_TC8_username_with_spaces_around():
    # 正常系：前後に空白を含むが正規化後は有効なユーザー名
    assert is_valid_username(" auser ") is True

# テストID: TC9
def test_TC9_one_character_username():
    # 正常系：1文字のユーザー名（最小長チェック）
    assert is_valid_username("a") is True

# テストID: TC10
def test_TC10_username_too_long():
    # 異常系：31文字以上の長いユーザー名（最大長超過）
    assert is_valid_username("aVeryLongUsernameWithMoreThanThirtyCharacters") is False

# テストID: TC11
def test_TC11_none_type():
    # 異常系：None型を渡した場合の型エラー
    with pytest.raises(TypeError):
        is_valid_username(None)

# テストID: TC12
def test_TC12_int_type():
    # 異常系：int型を渡した場合の型エラー
    with pytest.raises(TypeError):
        is_valid_username(123)

# テストID: TC13
def test_TC13_float_type():
    # 異常系：float型を渡した場合の型エラー
    with pytest.raises(TypeError):
        is_valid_username(12.34)

# テストID: TC14
def test_TC14_empty_list():
    # 異常系：空リストを渡した場合の型エラー
    with pytest.raises(TypeError):
        is_valid_username([])

# テストID: TC15
def test_TC15_empty_dict():
    # 異常系：空辞書を渡した場合の型エラー
    with pytest.raises(TypeError):
        is_valid_username({})

# テストID: TC16
def test_TC16_username_surrounded_by_underscores():
    # 正常系：アンダースコアで囲まれたユーザー名（正規表現が許容する場合）
    assert is_valid_username("_user_") is True

# テストID: TC17
def test_TC17_username_with_consecutive_periods():
    # 異常系：ピリオドが連続するユーザー名（正規表現が許容しない場合）
    assert is_valid_username("user..name") is False

# テストID: TC18
def test_TC18_username_with_consecutive_hyphens():
    # 異常系：ハイフンが連続するユーザー名（正規表現が許容しない場合）
    assert is_valid_username("user--name") is False

# テストID: TC19
def test_TC19_username_ends_with_underscore():
    # 正常系：アンダースコアで終わるユーザー名（正規表現が許容する場合）
    assert is_valid_username("user_name_") is True

# テストID: TC20
def test_TC20_username_ends_with_hyphen():
    # 正常系：許可された記号で終わるユーザー名（正規表現が許容する場合）
    assert is_valid_username("user.name-") is True

# テストID: TC21
def test_TC21_username_with_space_inside():
    # 異常系：空白を含むユーザー名（正規表現が許容しない場合）
    assert is_valid_username("user name") is False

# テストID: TC22
def test_TC22_username_with_invalid_symbol_sharp():
    # 異常系：許可されていない記号（#）を含むユーザー名
    assert is_valid_username("user#name") is False

# テストID: TC23
def test_TC23_username_ends_with_period():
    # 正常系：ピリオドで終わるユーザー名（正規表現が許容する場合）
    assert is_valid_username("user_name.") is True

# テストID: TC24
def test_TC24_username_ends_with_hyphen_and_underscore():
    # 正常系：ハイフンとアンダースコアで終わるユーザー名（正規表現が許容する場合）
    assert is_valid_username("user-name_") is True

# テストID: TC25
def test_TC25_username_with_consecutive_periods_and_hyphens():
    # 異常系：ピリオドとハイフンが連続するユーザー名（正規表現が許容しない場合）
    assert is_valid_username("user..name--") is False