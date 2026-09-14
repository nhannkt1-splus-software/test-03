import pytest

# テスト対象クラスのインポートを想定
# from your_module import InMemoryStore

# ダミーのProjectクラスを定義（型ヒント用）
class Project:
    pass

# InMemoryStoreのインスタンスを作成し、projects属性をセットアップするヘルパー
def create_store_with_projects():
    store = InMemoryStore()
    # projects属性が存在しない場合は追加
    if not hasattr(store, "projects"):
        store.projects = {}
    # project_id=1 のみ存在させる
    store.projects[1] = Project()
    return store

# --- 正常系・境界値・異常系（int型） ---

# TC1: 既存のproject_idを指定した場合
def test_get_project_existing_id():
    # TC1
    store = create_store_with_projects()
    # project_id=1は存在する
    result = store.get_project(1)
    # Project型のインスタンスが返ることを確認
    assert isinstance(result, Project)

# TC2: 存在しないproject_idを指定した場合
def test_get_project_non_existing_id():
    # TC2
    store = create_store_with_projects()
    # project_id=2は存在しない
    result = store.get_project(2)
    assert result is None

# TC3: 境界値（0）を指定した場合
def test_get_project_zero_id():
    # TC3
    store = create_store_with_projects()
    result = store.get_project(0)
    assert result is None

# TC4: 負のproject_idを指定した場合
def test_get_project_negative_id():
    # TC4
    store = create_store_with_projects()
    result = store.get_project(-1)
    assert result is None

# TC5: 非常に大きなproject_idを指定した場合
def test_get_project_large_id():
    # TC5
    store = create_store_with_projects()
    result = store.get_project(999999)
    assert result is None

# TC11: 極端に大きいproject_idを指定した場合
def test_get_project_extremely_large_id():
    # TC11
    store = create_store_with_projects()
    result = store.get_project(1000000000)
    assert result is None

# TC12: 極端に小さい負のproject_idを指定した場合
def test_get_project_extremely_negative_id():
    # TC12
    store = create_store_with_projects()
    result = store.get_project(-999999)
    assert result is None

# --- 型違い（TypeError期待） ---

# TC6: str型のproject_idを指定した場合
def test_get_project_str_id():
    # TC6
    store = create_store_with_projects()
    with pytest.raises(TypeError):
        store.get_project("1")

# TC7: NoneTypeのproject_idを指定した場合
def test_get_project_none_id():
    # TC7
    store = create_store_with_projects()
    with pytest.raises(TypeError):
        store.get_project(None)

# TC8: float型のproject_idを指定した場合
def test_get_project_float_id():
    # TC8
    store = create_store_with_projects()
    with pytest.raises(TypeError):
        store.get_project(1.5)

# TC9: list型のproject_idを指定した場合
def test_get_project_list_id():
    # TC9
    store = create_store_with_projects()
    with pytest.raises(TypeError):
        store.get_project([])

# TC10: dict型のproject_idを指定した場合
def test_get_project_dict_id():
    # TC10
    store = create_store_with_projects()
    with pytest.raises(TypeError):
        store.get_project({})
```
