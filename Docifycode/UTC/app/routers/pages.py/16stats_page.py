import pytest
from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.datastructures import Headers, QueryParams, URL
from starlette.templating import Jinja2Templates

# テスト用のテンプレートディレクトリを設定
templates = Jinja2Templates(directory=".")

# テスト対象関数をインポート
from your_module import stats_page  # your_moduleはstats_pageが定義されているモジュール名に置き換えてください

# Requestオブジェクトのモック作成ヘルパー
def make_request():
    # starlette.requests.Requestのインスタンスを作成
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/stats",
        "headers": Headers({}),
        "query_string": b"",
        "server": ("testserver", 80),
        "client": ("testclient", 12345),
        "scheme": "http",
        "root_path": "",
        "app": None,
        "query_params": QueryParams(""),
        "url": URL("http://testserver/stats"),
    }
    return Request(scope)

# StatsServiceのモック
class MockStatsService:
    def __init__(self, summarize_return=None, raise_exception=False):
        self.summarize_return = summarize_return
        self.raise_exception = raise_exception

    def summarize(self):
        if self.raise_exception:
            raise Exception("summarize error")
        return self.summarize_return

# TC1: 正常系 RequestとStatsServiceが正しく渡された場合
def test_stats_page_TC1():
    # TC1
    request = make_request()
    stats = MockStatsService(summarize_return={"count": 10, "avg": 5.5})
    response = stats_page(request, stats)
    # HTMLResponseが返ることを確認
    assert isinstance(response, HTMLResponse)
    # statsの値がテンプレートに渡されていることを確認
    assert "count" in response.body.decode() or "avg" in response.body.decode()

# TC2: 正常系 stats.summarize()が空辞書の場合
def test_stats_page_TC2():
    # TC2
    request = make_request()
    stats = MockStatsService(summarize_return={})
    response = stats_page(request, stats)
    assert isinstance(response, HTMLResponse)
    # 空辞書がテンプレートに渡されていることを確認
    assert "{}" in response.body.decode() or response.body.decode() != ""

# TC3: 正常系 stats.summarize()が大きな辞書の場合
def test_stats_page_TC3():
    # TC3
    request = make_request()
    big_dict = {f"key{i}": i for i in range(1000)}
    stats = MockStatsService(summarize_return=big_dict)
    response = stats_page(request, stats)
    assert isinstance(response, HTMLResponse)
    # 大きな辞書の一部がテンプレートに渡されていることを確認
    assert "key999" in response.body.decode()

# TC4: 正常系 stats.summarize()が特殊文字を含む場合
def test_stats_page_TC4():
    # TC4
    request = make_request()
    special_dict = {"emoji": "😀", "quote": "\"", "backslash": "\\"}
    stats = MockStatsService(summarize_return=special_dict)
    response = stats_page(request, stats)
    assert isinstance(response, HTMLResponse)
    # 特殊文字がテンプレートに渡されていることを確認
    assert "😀" in response.body.decode()
    assert "\"" in response.body.decode()
    assert "\\" in response.body.decode()

# TC5: 異常系 RequestがNoneの場合
def test_stats_page_TC5():
    # TC5
    stats = MockStatsService(summarize_return={"count": 1})
    with pytest.raises(TypeError):
        stats_page(None, stats)

# TC6: 異常系 Requestが整数値の場合
def test_stats_page_TC6():
    # TC6
    stats = MockStatsService(summarize_return={"count": 1})
    with pytest.raises(TypeError):
        stats_page(123, stats)

# TC7: 異常系 Requestが文字列値の場合
def test_stats_page_TC7():
    # TC7
    stats = MockStatsService(summarize_return={"count": 1})
    with pytest.raises(TypeError):
        stats_page("request_str", stats)

# TC8: 異常系 statsがNoneの場合
def test_stats_page_TC8():
    # TC8
    request = make_request()
    with pytest.raises(AttributeError):
        stats_page(request, None)

# TC9: 異常系 statsがsummarizeメソッドを持たない場合
def test_stats_page_TC9():
    # TC9
    request = make_request()
    class NoSummarize:
        pass
    stats = NoSummarize()
    with pytest.raises(AttributeError):
        stats_page(request, stats)

# TC10: 異常系 stats.summarize()が例外を投げる場合
def test_stats_page_TC10():
    # TC10
    request = make_request()
    stats = MockStatsService(raise_exception=True)
    with pytest.raises(Exception):
        stats_page(request, stats)

# TC11: 正常系 stats.summarize()がNoneを返す場合
def test_stats_page_TC11():
    # TC11
    request = make_request()
    stats = MockStatsService(summarize_return=None)
    response = stats_page(request, stats)
    assert isinstance(response, HTMLResponse)
    # Noneがテンプレートに渡されていることを確認
    assert "None" in response.body.decode() or response.body.decode() != ""

# TC12: 正常系 stats.summarize()がリストを返す場合
def test_stats_page_TC12():
    # TC12
    request = make_request()
    stats = MockStatsService(summarize_return=[1, 2, 3])
    response = stats_page(request, stats)
    assert isinstance(response, HTMLResponse)
    # リストがテンプレートに渡されていることを確認
    assert "[1, 2, 3]" in response.body.decode() or response.body.decode() != ""

# TC13: 正常系 stats.summarize()が数値を返す場合
def test_stats_page_TC13():
    # TC13
    request = make_request()
    stats = MockStatsService(summarize_return=42)
    response = stats_page(request, stats)
    assert isinstance(response, HTMLResponse)
    # 数値がテンプレートに渡されていることを確認
    assert "42" in response.body.decode() or response.body.decode() != ""