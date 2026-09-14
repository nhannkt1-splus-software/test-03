import pytest

# --- テスト用: DeskErrorのダミー定義（本番環境でimportされる場合は不要） ---
class DeskError(Exception):
    pass

# --- テスト対象クラスのインポートまたは再定義（スコープの都合でここに記載） ---
class DuplicateProjectError(DeskError):
    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Project slug {slug} already exists")

# --- 正常系・エッジケース: str型slugでインスタンス生成 ---
@pytest.mark.parametrize(
    "slug,expected_message,test_id",
    [
        # TC1: 一般的な英数字slug
        ("project-1", "Project slug project-1 already exists", "TC1"),
        # TC2: 日本語slug
        ("プロジェクトA", "Project slug プロジェクトA already exists", "TC2"),
        # TC3: 空文字slug
        ("", "Project slug  already exists", "TC3"),
        # TC4: 1文字slug
        ("a", "Project slug a already exists", "TC4"),
        # TC5: 100文字slug
        ("a"*100, f"Project slug {'a'*100} already exists", "TC5"),
        # TC10: 一般的な英数字slug（部分適用）
        ("project-1", "Project slug project-1 already exists", "TC10"),
        # TC11: 日本語slug（部分適用）
        ("プロジェクトA", "Project slug プロジェクトA already exists", "TC11"),
        # TC12: 空文字slug（部分適用）
        ("", "Project slug  already exists", "TC12"),
        # TC13: 1文字slug（部分適用）
        ("a", "Project slug a already exists", "TC13"),
        # TC14: 100文字slug（部分適用）
        ("a"*100, f"Project slug {'a'*100} already exists", "TC14"),
    ]
)
def test_DuplicateProjectError_str_slug(slug, expected_message, test_id):
    # --- {test_id} ---
    # slugがstr型の場合、インスタンス生成とメッセージ・属性を確認
    err = DuplicateProjectError(slug)
    # メッセージが正しいか
    assert str(err) == expected_message
    # slug属性が正しいか
    assert err.slug == slug

# --- 異常系: 非str型slugでTypeError発生を確認 ---
@pytest.mark.parametrize(
    "slug,test_id",
    [
        # TC6: int型
        (123, "TC6"),
        # TC7: None型
        (None, "TC7"),
        # TC8: list型
        ([], "TC8"),
        # TC9: dict型
        ({}, "TC9"),
        # TC15: int型（部分適用）
        (123, "TC15"),
        # TC16: None型（部分適用）
        (None, "TC16"),
        # TC17: list型（部分適用）
        ([], "TC17"),
        # TC18: dict型（部分適用）
        ({}, "TC18"),
    ]
)
def test_DuplicateProjectError_non_str_slug(slug, test_id):
    # --- {test_id} ---
    # slugがstr型以外の場合、TypeErrorが発生することを確認
    with pytest.raises(TypeError):
        DuplicateProjectError(slug)
```
