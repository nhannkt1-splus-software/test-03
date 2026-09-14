import pytest

# テスト対象のTicketService, TicketStatus, Ticketクラスをインポート
from your_module import TicketService, TicketStatus

# TC1: title, descriptionの前後空白が除去されるケース
def test_create_ticket_strips_whitespace_TC1():
    # 前後空白あり
    service = TicketService()
    ticket = service.create_ticket(title="  New bug  ", description="  overflow  ")
    assert ticket.title == "New bug"  # TC1
    assert ticket.description == "overflow"  # TC1
    assert ticket.status == TicketStatus.OPEN  # TC1

# TC2: title, descriptionが空白なしの文字列
def test_create_ticket_no_whitespace_TC2():
    service = TicketService()
    ticket = service.create_ticket(title="New bug", description="overflow")
    assert ticket.title == "New bug"  # TC2
    assert ticket.description == "overflow"  # TC2
    assert ticket.status == TicketStatus.OPEN  # TC2

# TC3: title, descriptionが空白のみの場合、空文字列になる
def test_create_ticket_only_whitespace_TC3():
    service = TicketService()
    ticket = service.create_ticket(title="   ", description="   ")
    assert ticket.title == ""  # TC3
    assert ticket.description == ""  # TC3
    assert ticket.status == TicketStatus.OPEN  # TC3

# TC4: title, descriptionが空文字列
def test_create_ticket_empty_string_TC4():
    service = TicketService()
    ticket = service.create_ticket(title="", description="")
    assert ticket.title == ""  # TC4
    assert ticket.description == ""  # TC4
    assert ticket.status == TicketStatus.OPEN  # TC4

# TC5: titleがNone型の場合
def test_create_ticket_title_none_TC5():
    service = TicketService()
    with pytest.raises(TypeError):  # TC5
        service.create_ticket(title=None, description="overflow")

# TC6: descriptionがNone型の場合
def test_create_ticket_description_none_TC6():
    service = TicketService()
    with pytest.raises(TypeError):  # TC6
        service.create_ticket(title="New bug", description=None)

# TC7: titleがint型の場合
def test_create_ticket_title_int_TC7():
    service = TicketService()
    with pytest.raises(TypeError):  # TC7
        service.create_ticket(title=123, description="overflow")

# TC8: descriptionがint型の場合
def test_create_ticket_description_int_TC8():
    service = TicketService()
    with pytest.raises(TypeError):  # TC8
        service.create_ticket(title="New bug", description=456)

# TC9: titleがlist型の場合
def test_create_ticket_title_list_TC9():
    service = TicketService()
    with pytest.raises(TypeError):  # TC9
        service.create_ticket(title=["bug"], description="overflow")

# TC10: descriptionがdict型の場合
def test_create_ticket_description_dict_TC10():
    service = TicketService()
    with pytest.raises(TypeError):  # TC10
        service.create_ticket(title="New bug", description={"desc": "overflow"})

# TC11: serviceがNone型の場合
def test_create_ticket_service_none_TC11():
    with pytest.raises(AttributeError):  # TC11
        # None型なのでcreate_ticketメソッドが存在しない
        service = None
        service.create_ticket(title="New bug", description="overflow")

# TC12: descriptionが空白のみの場合、空文字列になる
def test_create_ticket_description_only_whitespace_TC12():
    service = TicketService()
    ticket = service.create_ticket(title="New bug", description="   ")
    assert ticket.title == "New bug"  # TC12
    assert ticket.description == ""  # TC12
    assert ticket.status == TicketStatus.OPEN  # TC12

# TC13: titleが空白のみの場合、空文字列になる
def test_create_ticket_title_only_whitespace_TC13():
    service = TicketService()
    ticket = service.create_ticket(title="   ", description="overflow")
    assert ticket.title == ""  # TC13
    assert ticket.description == "overflow"  # TC13
    assert ticket.status == TicketStatus.OPEN  # TC13

# TC14: titleが空文字列の場合
def test_create_ticket_title_empty_string_TC14():
    service = TicketService()
    ticket = service.create_ticket(title="", description="overflow")
    assert ticket.title == ""  # TC14
    assert ticket.description == "overflow"  # TC14
    assert ticket.status == TicketStatus.OPEN  # TC14

# TC15: descriptionが空文字列の場合
def test_create_ticket_description_empty_string_TC15():
    service = TicketService()
    ticket = service.create_ticket(title="New bug", description="")
    assert ticket.title == "New bug"  # TC15
    assert ticket.description == ""  # TC15
    assert ticket.status == TicketStatus.OPEN  # TC15