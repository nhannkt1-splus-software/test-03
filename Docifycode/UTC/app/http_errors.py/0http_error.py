import pytest

# --- テスト用ダミークラスと定数の定義 ---
# FastAPIやStarletteのHTTPExceptionとstatusを模倣
class HTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

class status:
    HTTP_404_NOT_FOUND = 404
    HTTP_400_BAD_REQUEST = 400
    HTTP_409_CONFLICT = 409

# テスト用例外クラス
class _NOT_FOUND(Exception):
    pass

class _BAD_REQUEST(Exception):
    pass

class _CONFLICT(Exception):
    pass

class DeskError(Exception):
    pass

# --- テスト対象関数のインポート ---
# テスト対象関数が同じファイルにある場合
from your_module import http_error  # your_moduleは適宜置き換えてください

# --- テストケース ---
# TC1: _NOT_FOUND型の例外インスタンス
def test_http_error_tc1():
    # TC1
    exc = _NOT_FOUND()
    result = http_error(exc)
    # 期待値: 404, detailはstr(exc)
    assert isinstance(result, HTTPException)
    assert result.status_code == status.HTTP_404_NOT_FOUND
    assert result.detail == str(exc)

# TC2: _BAD_REQUEST型の例外インスタンス
def test_http_error_tc2():
    # TC2
    exc = _BAD_REQUEST()
    result = http_error(exc)
    assert isinstance(result, HTTPException)
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert result.detail == str(exc)

# TC3: _CONFLICT型の例外インスタンス
def test_http_error_tc3():
    # TC3
    exc = _CONFLICT()
    result = http_error(exc)
    assert isinstance(result, HTTPException)
    assert result.status_code == status.HTTP_409_CONFLICT
    assert result.detail == str(exc)

# TC4: DeskError型の例外インスタンス
def test_http_error_tc4():
    # TC4
    exc = DeskError('desk error message')
    result = http_error(exc)
    assert isinstance(result, HTTPException)
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert result.detail == str(exc)

# TC5: Exception型の例外インスタンス
def test_http_error_tc5():
    # TC5
    exc = Exception('generic error')
    with pytest.raises(Exception) as e:
        http_error(exc)
    assert str(e.value) == 'generic error'

# TC6: ValueError型の例外インスタンス
def test_http_error_tc6():
    # TC6
    exc = ValueError('value error')
    with pytest.raises(ValueError) as e:
        http_error(exc)
    assert str(e.value) == 'value error'

# TC7: int型（型不一致）
def test_http_error_tc7():
    # TC7
    exc = 123
    with pytest.raises(TypeError):
        http_error(exc)

# TC8: None（型不一致）
def test_http_error_tc8():
    # TC8
    exc = None
    with pytest.raises(TypeError):
        http_error(exc)

# TC9: str型（型不一致）
def test_http_error_tc9():
    # TC9
    exc = 'string error'
    with pytest.raises(TypeError):
        http_error(exc)

# TC10: 引数なしのException型インスタンス
def test_http_error_tc10():
    # TC10
    exc = Exception()
    with pytest.raises(Exception) as e:
        http_error(exc)
    # detailは空文字列
    assert str(e.value) == ''

# TC11: 空文字のDeskError型インスタンス
def test_http_error_tc11():
    # TC11
    exc = DeskError('')
    result = http_error(exc)
    assert isinstance(result, HTTPException)
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert result.detail == ''

# TC12: detail付き_NOT_FOUND型の例外インスタンス
def test_http_error_tc12():
    # TC12
    exc = _NOT_FOUND('not found message')
    result = http_error(exc)
    assert isinstance(result, HTTPException)
    assert result.status_code == status.HTTP_404_NOT_FOUND
    assert result.detail == 'not found message'

# TC13: detail付き_BAD_REQUEST型の例外インスタンス
def test_http_error_tc13():
    # TC13
    exc = _BAD_REQUEST('bad request message')
    result = http_error(exc)
    assert isinstance(result, HTTPException)
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert result.detail == 'bad request message'

# TC14: detail付き_CONFLICT型の例外インスタンス
def test_http_error_tc14():
    # TC14
    exc = _CONFLICT('conflict message')
    result = http_error(exc)
    assert isinstance(result, HTTPException)
    assert result.status_code == status.HTTP_409_CONFLICT
    assert result.detail == 'conflict message'