import pytest

# --- テスト用のダミーEnum定義 ---
import enum

class Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TicketStatus(enum.Enum):
    OPEN = 1
    CLOSED = 2

# --- テスト対象関数のimport ---
import sys

# テスト対象関数を直接importできる場合
# from <target_module> import _board_context

# ここでは問題文の関数を直接定義して使う
def _board_context(
    tickets,
    members,
    projects,
    error: str | None = None,
):
    return {
        "tickets": tickets,
        "members": members,
        "projects": [project for project in projects if not project.archived],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": error,
    }

# --- dictのarchived属性を持つダミーオブジェクト ---
class ProjectObj:
    def __init__(self, d):
        self.__dict__.update(d)

# --- テストケース ---

# TC1: 全て空リストとNone
def test_board_context_TC1():
    # テストID: TC1
    tickets = []
    members = []
    projects = []
    error = None
    expected = {
        "tickets": [],
        "members": [],
        "projects": [],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC2: projectsにarchived=Falseのみ
def test_board_context_TC2():
    # テストID: TC2
    tickets = ["ticket1"]
    members = ["member1"]
    projects = [ProjectObj({"archived": False})]
    error = None
    expected = {
        "tickets": ["ticket1"],
        "members": ["member1"],
        "projects": [projects[0]],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC3: projectsにarchived=Trueのみ
def test_board_context_TC3():
    # テストID: TC3
    tickets = ["ticket1"]
    members = ["member1"]
    projects = [ProjectObj({"archived": True})]
    error = None
    expected = {
        "tickets": ["ticket1"],
        "members": ["member1"],
        "projects": [],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC4: projectsにarchivedのTrue/False混在
def test_board_context_TC4():
    # テストID: TC4
    tickets = ["ticket1"]
    members = ["member1"]
    p0 = ProjectObj({"archived": False})
    p1 = ProjectObj({"archived": True})
    projects = [p0, p1]
    error = None
    expected = {
        "tickets": ["ticket1"],
        "members": ["member1"],
        "projects": [p0],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC5: errorに文字列
def test_board_context_TC5():
    # テストID: TC5
    tickets = ["ticket1", "ticket2"]
    members = ["member1", "member2"]
    p0 = ProjectObj({"archived": False})
    p1 = ProjectObj({"archived": False})
    projects = [p0, p1]
    error = "エラー内容"
    expected = {
        "tickets": ["ticket1", "ticket2"],
        "members": ["member1", "member2"],
        "projects": [p0, p1],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": "エラー内容",
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC6: ticketsがNone
def test_board_context_TC6():
    # テストID: TC6
    tickets = None
    members = []
    projects = []
    error = None
    expected = {
        "tickets": None,
        "members": [],
        "projects": [],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC7: membersがNone
def test_board_context_TC7():
    # テストID: TC7
    tickets = []
    members = None
    projects = []
    error = None
    expected = {
        "tickets": [],
        "members": None,
        "projects": [],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC8: projectsがNone（TypeError）
def test_board_context_TC8():
    # テストID: TC8
    tickets = []
    members = []
    projects = None
    error = None
    with pytest.raises(TypeError):
        _board_context(tickets, members, projects, error)

# TC9: errorがint型
def test_board_context_TC9():
    # テストID: TC9
    tickets = []
    members = []
    projects = []
    error = 123
    expected = {
        "tickets": [],
        "members": [],
        "projects": [],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": 123,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC10: ticketsがstr型
def test_board_context_TC10():
    # テストID: TC10
    tickets = "not_a_list"
    members = []
    projects = []
    error = None
    expected = {
        "tickets": "not_a_list",
        "members": [],
        "projects": [],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC11: membersがstr型
def test_board_context_TC11():
    # テストID: TC11
    tickets = []
    members = "not_a_list"
    projects = []
    error = None
    expected = {
        "tickets": [],
        "members": "not_a_list",
        "projects": [],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC12: projectsがstr型（TypeError）
def test_board_context_TC12():
    # テストID: TC12
    tickets = []
    members = []
    projects = "not_a_list"
    error = None
    # projectsがstr型の場合、for project in projectsで各文字に対してarchived属性アクセスしようとするためAttributeError
    with pytest.raises(AttributeError):
        _board_context(tickets, members, projects, error)

# TC13: projectsの要素にarchived属性がない（AttributeError）
def test_board_context_TC13():
    # テストID: TC13
    tickets = []
    members = []
    # dictにarchived属性がない
    projects = [ProjectObj({"no_archived": True})]
    error = None
    with pytest.raises(AttributeError):
        _board_context(tickets, members, projects, error)

# TC14: projectsの要素がint型（AttributeError）
def test_board_context_TC14():
    # テストID: TC14
    tickets = []
    members = []
    projects = [123]
    error = None
    with pytest.raises(AttributeError):
        _board_context(tickets, members, projects, error)

# TC15: projectsの要素がNone（AttributeError）
def test_board_context_TC15():
    # テストID: TC15
    tickets = []
    members = []
    projects = [None]
    error = None
    with pytest.raises(AttributeError):
        _board_context(tickets, members, projects, error)

# TC16: projectsのarchivedがnull
def test_board_context_TC16():
    # テストID: TC16
    tickets = []
    members = []
    projects = [ProjectObj({"archived": None})]
    error = None
    expected = {
        "tickets": [],
        "members": [],
        "projects": [projects[0]],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC17: projectsのarchivedが0（False相当）
def test_board_context_TC17():
    # テストID: TC17
    tickets = []
    members = []
    projects = [ProjectObj({"archived": 0})]
    error = None
    expected = {
        "tickets": [],
        "members": [],
        "projects": [projects[0]],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC18: projectsのarchivedが1（True相当）
def test_board_context_TC18():
    # テストID: TC18
    tickets = []
    members = []
    projects = [ProjectObj({"archived": 1})]
    error = None
    expected = {
        "tickets": [],
        "members": [],
        "projects": [],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC19: projectsのarchivedが文字列'False'
def test_board_context_TC19():
    # テストID: TC19
    tickets = []
    members = []
    projects = [ProjectObj({"archived": "False"})]
    error = None
    expected = {
        "tickets": [],
        "members": [],
        "projects": [projects[0]],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected

# TC20: projectsのarchivedが文字列'True'
def test_board_context_TC20():
    # テストID: TC20
    tickets = []
    members = []
    projects = [ProjectObj({"archived": "True"})]
    error = None
    expected = {
        "tickets": [],
        "members": [],
        "projects": [projects[0]],
        "priorities": list(Priority),
        "statuses": list(TicketStatus),
        "error": None,
    }
    result = _board_context(tickets, members, projects, error)
    assert result == expected