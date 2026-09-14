import pytest

# テスト対象のクラス・列挙型・例外をインポート
from target_module import TicketService, TicketStatus, Priority, TicketClosedError

# TC1: CLOSED状態のチケットに対してupdate_ticketを実行し、TicketClosedErrorが発生するケース
def test_TC1_update_closed_ticket():
    # チケット作成と状態変更
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.change_status(ticket.id, TicketStatus.IN_PROGRESS)
    service.change_status(ticket.id, TicketStatus.RESOLVED)
    service.change_status(ticket.id, TicketStatus.CLOSED)
    # update_ticketで例外発生を確認
    with pytest.raises(TicketClosedError):
        service.update_ticket(ticket.id, priority=Priority.HIGH)

# TC2: CLOSED状態のチケットに対してadd_commentを実行し、TicketClosedErrorが発生するケース
def test_TC2_add_comment_closed_ticket():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.change_status(ticket.id, TicketStatus.IN_PROGRESS)
    service.change_status(ticket.id, TicketStatus.RESOLVED)
    service.change_status(ticket.id, TicketStatus.CLOSED)
    with pytest.raises(TicketClosedError):
        service.add_comment(ticket.id, "too late", "maya")

# TC3: CLOSED状態のチケットに対してdelete_ticketを実行し、TicketClosedErrorが発生するケース
def test_TC3_delete_closed_ticket():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.change_status(ticket.id, TicketStatus.IN_PROGRESS)
    service.change_status(ticket.id, TicketStatus.RESOLVED)
    service.change_status(ticket.id, TicketStatus.CLOSED)
    with pytest.raises(TicketClosedError):
        service.delete_ticket(ticket.id)

# TC4: IN_PROGRESS状態のチケットに対してupdate_ticketを実行し、正常に更新されるケース
def test_TC4_update_in_progress_ticket():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.change_status(ticket.id, TicketStatus.IN_PROGRESS)
    # 更新が正常に行われることを確認
    service.update_ticket(ticket.id, priority=Priority.HIGH)
    updated_ticket = service.get_ticket(ticket.id)
    assert updated_ticket.priority == Priority.HIGH

# TC5: RESOLVED状態のチケットに対してadd_commentを実行し、正常にコメントが追加されるケース
def test_TC5_add_comment_resolved_ticket():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.change_status(ticket.id, TicketStatus.IN_PROGRESS)
    service.change_status(ticket.id, TicketStatus.RESOLVED)
    service.add_comment(ticket.id, "too late", "maya")
    comments = service.get_comments(ticket.id)
    assert any(c['author'] == "maya" and c['comment'] == "too late" for c in comments)

# TC6: OPEN状態のチケットに対してdelete_ticketを実行し、正常に削除されるケース
def test_TC6_delete_open_ticket():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.delete_ticket(ticket.id)
    with pytest.raises(ValueError):
        service.get_ticket(ticket.id)

# TC7: 存在しないチケットIDでupdate_ticketを実行し、ValueErrorが発生するケース
def test_TC7_update_nonexistent_ticket():
    service = TicketService()
    with pytest.raises(ValueError):
        service.update_ticket(999, priority=Priority.HIGH)

# TC8: ticket.idが型不一致の場合にupdate_ticketを実行し、TypeErrorが発生するケース
def test_TC8_update_ticket_id_type_error():
    service = TicketService()
    with pytest.raises(TypeError):
        service.update_ticket("abc", priority=Priority.HIGH)

# TC9: priorityが型不一致の場合にupdate_ticketを実行し、TypeErrorが発生するケース
def test_TC9_update_ticket_priority_type_error():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    with pytest.raises(TypeError):
        service.update_ticket(ticket.id, priority="invalid_priority")

# TC10: commentが型不一致の場合にadd_commentを実行し、TypeErrorが発生するケース
def test_TC10_add_comment_type_error():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    with pytest.raises(TypeError):
        service.add_comment(ticket.id, 123, "maya")

# TC11: authorが型不一致の場合にadd_commentを実行し、TypeErrorが発生するケース
def test_TC11_add_comment_author_type_error():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    with pytest.raises(TypeError):
        service.add_comment(ticket.id, "too late", 456)

# TC12: 存在しないチケットIDでdelete_ticketを実行し、ValueErrorが発生するケース
def test_TC12_delete_nonexistent_ticket():
    service = TicketService()
    with pytest.raises(ValueError):
        service.delete_ticket(999)

# TC13: ticket.idが型不一致の場合にdelete_ticketを実行し、TypeErrorが発生するケース
def test_TC13_delete_ticket_id_type_error():
    service = TicketService()
    with pytest.raises(TypeError):
        service.delete_ticket("abc")

# TC14: 存在しないチケットIDでadd_commentを実行し、ValueErrorが発生するケース
def test_TC14_add_comment_nonexistent_ticket():
    service = TicketService()
    with pytest.raises(ValueError):
        service.add_comment(999, "too late", "maya")

# TC15: ticket.idが型不一致の場合にadd_commentを実行し、TypeErrorが発生するケース
def test_TC15_add_comment_ticket_id_type_error():
    service = TicketService()
    with pytest.raises(TypeError):
        service.add_comment("abc", "too late", "maya")

# TC16: 存在しないチケットIDでupdate_ticketを実行し、ValueErrorが発生するケース（重複確認用）
def test_TC16_update_nonexistent_ticket_duplicate():
    service = TicketService()
    with pytest.raises(ValueError):
        service.update_ticket(999, priority=Priority.HIGH)

# TC17: OPEN状態のチケットに対してupdate_ticketを実行し、正常に更新されるケース
def test_TC17_update_open_ticket():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.update_ticket(ticket.id, priority=Priority.HIGH)
    updated_ticket = service.get_ticket(ticket.id)
    assert updated_ticket.priority == Priority.HIGH

# TC18: IN_PROGRESS状態のチケットに対してadd_commentを実行し、正常にコメントが追加されるケース
def test_TC18_add_comment_in_progress_ticket():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.change_status(ticket.id, TicketStatus.IN_PROGRESS)
    service.add_comment(ticket.id, "too late", "maya")
    comments = service.get_comments(ticket.id)
    assert any(c['author'] == "maya" and c['comment'] == "too late" for c in comments)

# TC19: OPEN状態のチケットに対してadd_commentを実行し、正常にコメントが追加されるケース
def test_TC19_add_comment_open_ticket():
    service = TicketService()
    ticket = service.create_ticket(title="Lock me")
    service.add_comment(ticket.id, "too late", "maya")
    comments = service.get_comments(ticket.id)
    assert any(c['author'] == "maya" and c['comment'] == "too late" for c in comments)