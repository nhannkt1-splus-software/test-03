import pytest

# テスト用ダミークラスと関数の定義
class TicketStatus:
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

class Priority:
    HIGH = 'HIGH'
    LOW = 'LOW'

class Ticket:
    def __init__(
        self,
        id,
        status=None,
        priority=None,
        project_id=None,
        title='',
        description='',
        assignee=None
    ):
        self.id = id
        self.status = status
        self.priority = priority
        self.project_id = project_id
        self.title = title
        self.description = description
        self.assignee = assignee

# is_overdue関数のモック
def is_overdue(ticket):
    # テストケースごとに差し替える
    return getattr(ticket, '_is_overdue', False)

# TicketServiceのテスト用インスタンス生成ヘルパー
def make_service(store_list, is_overdue_func=None):
    class DummyStore:
        def list_all(self):
            return store_list
    service = TicketService.__new__(TicketService)
    service.store = DummyStore()
    # is_overdueを差し替え
    global is_overdue
    if is_overdue_func:
        is_overdue = is_overdue_func
    else:
        is_overdue = lambda ticket: getattr(ticket, '_is_overdue', False)
    return service

# TC1: 全てのフィルタがNoneで、チケットが存在しない場合の正常系
def test_TC1():
    # テストID: TC1
    service = make_service([])
    result = service.list_tickets()
    assert result == []

# TC2: 全てのフィルタがNoneで、複数件のチケットが返る正常系
def test_TC2():
    # テストID: TC2
    t1 = Ticket(id=1)
    t2 = Ticket(id=2)
    service = make_service([t1, t2])
    result = service.list_tickets()
    assert result == [t1, t2]

# TC3: statusによるフィルタの正常系
def test_TC3():
    # テストID: TC3
    t1 = Ticket(id=1, status=TicketStatus.OPEN)
    t2 = Ticket(id=2, status=TicketStatus.CLOSED)
    service = make_service([t1, t2])
    result = service.list_tickets(status=TicketStatus.OPEN)
    assert result == [t1]

# TC4: statusによるフィルタの正常系（別値）
def test_TC4():
    # テストID: TC4
    t1 = Ticket(id=1, status=TicketStatus.OPEN)
    t2 = Ticket(id=2, status=TicketStatus.CLOSED)
    service = make_service([t1, t2])
    result = service.list_tickets(status=TicketStatus.CLOSED)
    assert result == [t2]

# TC5: statusが不正な型の場合の異常系
def test_TC5():
    # テストID: TC5
    t1 = Ticket(id=1)
    service = make_service([t1])
    with pytest.raises(TypeError):
        service.list_tickets(status='invalid_status')

# TC6: priorityによるフィルタの正常系
def test_TC6():
    # テストID: TC6
    t1 = Ticket(id=1, priority=Priority.HIGH)
    t2 = Ticket(id=2, priority=Priority.LOW)
    service = make_service([t1, t2])
    result = service.list_tickets(priority=Priority.HIGH)
    assert result == [t1]

# TC7: priorityが不正な型の場合の異常系
def test_TC7():
    # テストID: TC7
    t1 = Ticket(id=1)
    service = make_service([t1])
    with pytest.raises(TypeError):
        service.list_tickets(priority=123)

# TC8: project_idによるフィルタの正常系
def test_TC8():
    # テストID: TC8
    t1 = Ticket(id=1, project_id=1)
    t2 = Ticket(id=2, project_id=2)
    service = make_service([t1, t2])
    result = service.list_tickets(project_id=1)
    assert result == [t1]

# TC9: project_idが不正な型の場合の異常系
def test_TC9():
    # テストID: TC9
    t1 = Ticket(id=1)
    service = make_service([t1])
    with pytest.raises(TypeError):
        service.list_tickets(project_id='abc')

# TC10: qによる部分一致フィルタの正常系
def test_TC10():
    # テストID: TC10
    t1 = Ticket(id=1, title='Test ticket', description='desc', assignee='user')
    t2 = Ticket(id=2, title='Other', description='test', assignee='user')
    service = make_service([t1, t2])
    result = service.list_tickets(q='test')
    assert result == [t1, t2]

# TC11: qの前後空白が除去されるケース
def test_TC11():
    # テストID: TC11
    t1 = Ticket(id=1, title='Test ticket', description='desc', assignee='user')
    service = make_service([t1])
    result = service.list_tickets(q='  TEST  ')
    assert result == [t1]

# TC12: qが空文字列の場合の正常系
def test_TC12():
    # テストID: TC12
    t1 = Ticket(id=1)
    service = make_service([t1])
    result = service.list_tickets(q='')
    assert result == [t1]

# TC13: qが不正な型の場合の異常系
def test_TC13():
    # テストID: TC13
    t1 = Ticket(id=1)
    service = make_service([t1])
    with pytest.raises(TypeError):
        service.list_tickets(q=123)

# TC14: overdue=Trueで期限切れチケットのみ返す正常系
def test_TC14():
    # テストID: TC14
    t1 = Ticket(id=1)
    t1._is_overdue = True
    t2 = Ticket(id=2)
    t2._is_overdue = False
    service = make_service([t1, t2])
    result = service.list_tickets(overdue=True)
    assert result == [t1]

# TC15: overdue=Falseで期限内のみ返す正常系
def test_TC15():
    # テストID: TC15
    t1 = Ticket(id=1)
    t1._is_overdue = True
    t2 = Ticket(id=2)
    t2._is_overdue = False
    service = make_service([t1, t2])
    result = service.list_tickets(overdue=False)
    assert result == [t2]

# TC16: overdueが不正な型の場合の異常系
def test_TC16():
    # テストID: TC16
    t1 = Ticket(id=1)
    service = make_service([t1])
    with pytest.raises(TypeError):
        service.list_tickets(overdue='true')

# TC17: 全てのフィルタを指定した正常系
def test_TC17():
    # テストID: TC17
    t1 = Ticket(id=1, status=TicketStatus.OPEN, priority=Priority.HIGH, project_id=1, title='test', description='desc', assignee='user')
    t1._is_overdue = True
    t2 = Ticket(id=2, status=TicketStatus.OPEN, priority=Priority.HIGH, project_id=1, title='other', description='desc', assignee='user')
    t2._is_overdue = False
    service = make_service([t1, t2])
    result = service.list_tickets(
        status=TicketStatus.OPEN,
        priority=Priority.HIGH,
        project_id=1,
        q='test',
        overdue=True
    )
    assert result == [t1]

# TC18: 返却値がidで昇順ソートされることの確認
def test_TC18():
    # テストID: TC18
    t1 = Ticket(id=1)
    t2 = Ticket(id=2)
    service = make_service([t2, t1])  # 降順で渡す
    result = service.list_tickets()
    assert result == [t1, t2]

# TC19: 1件のみ存在する場合の正常系
def test_TC19():
    # テストID: TC19
    t1 = Ticket(id=1)
    service = make_service([t1])
    result = service.list_tickets()
    assert result == [t1]

# TC20: store.list_all()がNoneの場合の異常系
def test_TC20():
    # テストID: TC20
    class DummyStore:
        def list_all(self):
            return None
    service = TicketService.__new__(TicketService)
    service.store = DummyStore()
    with pytest.raises(AttributeError):
        service.list_tickets()

# TC21: チケットオブジェクトの属性不足による異常系
def test_TC21():
    # テストID: TC21
    class IncompleteTicket:
        def __init__(self, id):
            self.id = id
    t1 = IncompleteTicket(id=1)
    service = make_service([t1])
    with pytest.raises(AttributeError):
        service.list_tickets(status=TicketStatus.OPEN)

# TC22: project_idの境界値によるフィルタの正常系
def test_TC22():
    # テストID: TC22
    t1 = Ticket(id=1, project_id=999999)
    t2 = Ticket(id=2, project_id=1)
    service = make_service([t1, t2])
    result = service.list_tickets(project_id=999999)
    assert result == [t1]

# TC23: store.list_all()が1件のみ返す場合の正常系（重複確認）
def test_TC23():
    # テストID: TC23
    t1 = Ticket(id=1)
    service = make_service([t1])
    result = service.list_tickets()
    assert result == [t1]

# TC24: store.list_all()が昇順でない場合でも返却値が昇順になることの確認（重複確認）
def test_TC24():
    # テストID: TC24
    t1 = Ticket(id=1)
    t2 = Ticket(id=2)
    service = make_service([t2, t1])
    result = service.list_tickets()
    assert result == [t1, t2]

# TC25: store.list_all()が昇順で返す場合の正常系（重複確認）
def test_TC25():
    # テストID: TC25
    t1 = Ticket(id=1)
    t2 = Ticket(id=2)
    service = make_service([t1, t2])
    result = service.list_tickets()
    assert result == [t1, t2]

# TC26: store.list_all()が複数件返す場合の正常系（重複確認）
def test_TC26():
    # テストID: TC26
    t1 = Ticket(id=1)
    t2 = Ticket(id=2)
    service = make_service([t1, t2])
    result = service.list_tickets()
    assert result == [t1, t2]

# TC27: store.list_all()が1件のみ返す場合の正常系（重複確認）
def test_TC27():
    # テストID: TC27
    t1 = Ticket(id=1)
    service = make_service([t1])
    result = service.list_tickets()
    assert result == [t1]

# TC28: store.list_all()が空リストの場合の正常系（重複確認）
def test_TC28():
    # テストID: TC28
    service = make_service([])
    result = service.list_tickets()
    assert result == []