import pytest

# テストID: TC1
# 正常系：チケットのステータス変更が許可されたパスで全て成功するケース
def test_TC1_change_status_follows_allowed_path(mocker):
    # TicketService, TicketStatusのモックを用意
    TicketService = mocker.Mock()
    TicketStatus = mocker.Mock()
    # チケットインスタンスのモック
    ticket = mocker.Mock()
    ticket.id = 1
    closed_ticket = mocker.Mock()
    closed_ticket.status = TicketStatus.CLOSED

    # create_ticket, change_statusの戻り値を設定
    TicketService.create_ticket.return_value = ticket
    TicketService.change_status.side_effect = [
        None,  # IN_PROGRESS
        None,  # RESOLVED
        closed_ticket  # CLOSED
    ]

    # test_change_status_follows_allowed_pathを実行
    from target import test_change_status_follows_allowed_path
    test_change_status_follows_allowed_path(TicketService)

    # create_ticket, change_statusが正しく呼ばれたか確認
    TicketService.create_ticket.assert_called_once_with(title="Move me")
    assert TicketService.change_status.call_count == 3
    assert closed_ticket.status == TicketStatus.CLOSED

# テストID: TC2
# 異常系：serviceがNone型の場合の型不一致テスト
def test_TC2_service_is_none():
    from target import test_change_status_follows_allowed_path
    with pytest.raises(TypeError):
        test_change_status_follows_allowed_path(None)

# テストID: TC3
# 異常系：serviceがint型の場合の型不一致テスト
def test_TC3_service_is_int():
    from target import test_change_status_follows_allowed_path
    with pytest.raises(TypeError):
        test_change_status_follows_allowed_path(123)

# テストID: TC4
# 異常系：serviceがstr型の場合の型不一致テスト
def test_TC4_service_is_str():
    from target import test_change_status_follows_allowed_path
    with pytest.raises(TypeError):
        test_change_status_follows_allowed_path('test')

# テストID: TC5
# 異常系：create_ticketが失敗するケース（例外発生）
def test_TC5_create_ticket_failure(mocker):
    TicketService = mocker.Mock()
    TicketService.create_ticket.side_effect = ValueError("Invalid ticket creation")
    from target import test_change_status_follows_allowed_path
    with pytest.raises(ValueError):
        test_change_status_follows_allowed_path(TicketService)

# テストID: TC6
# 異常系：change_statusが失敗するケース（例外発生）
def test_TC6_change_status_failure(mocker):
    TicketService = mocker.Mock()
    ticket = mocker.Mock()
    ticket.id = 1
    TicketService.create_ticket.return_value = ticket
    # change_statusの2回目で例外発生
    TicketService.change_status.side_effect = [
        None,  # IN_PROGRESS
        ValueError("Invalid status change")  # RESOLVED
    ]
    from target import test_change_status_follows_allowed_path
    with pytest.raises(ValueError):
        test_change_status_follows_allowed_path(TicketService)

# テストID: TC7
# 異常系：サービス内部で予期しない例外が発生するケース（例：DB接続失敗）
def test_TC7_service_internal_exception(mocker):
    TicketService = mocker.Mock()
    TicketService.create_ticket.side_effect = RuntimeError("DB connection failed")
    from target import test_change_status_follows_allowed_path
    with pytest.raises(RuntimeError):
        test_change_status_follows_allowed_path(TicketService)

# テストID: TC8
# 異常系：最終ステータスがCLOSEDでない場合のアサーションエラー
def test_TC8_closed_status_not_closed(mocker):
    TicketService = mocker.Mock()
    TicketStatus = mocker.Mock()
    ticket = mocker.Mock()
    ticket.id = 1
    closed_ticket = mocker.Mock()
    closed_ticket.status = TicketStatus.IN_PROGRESS  # CLOSEDでない

    TicketService.create_ticket.return_value = ticket
    TicketService.change_status.side_effect = [
        None,  # IN_PROGRESS
        None,  # RESOLVED
        closed_ticket  # CLOSED
    ]
    from target import test_change_status_follows_allowed_path
    with pytest.raises(AssertionError):
        test_change_status_follows_allowed_path(TicketService)

# テストID: TC9
# 異常系：change_statusが許可されていないステータス遷移を試みた場合の例外
def test_TC9_change_status_invalid_transition(mocker):
    TicketService = mocker.Mock()
    ticket = mocker.Mock()
    ticket.id = 1
    TicketService.create_ticket.return_value = ticket
    # change_statusの2回目で許可されていない遷移
    TicketService.change_status.side_effect = [
        None,  # IN_PROGRESS
        ValueError("Invalid status transition")  # RESOLVED
    ]
    from target import test_change_status_follows_allowed_path
    with pytest.raises(ValueError):
        test_change_status_follows_allowed_path(TicketService)

# テストID: TC10
# 異常系：create_ticketでタイトルが空文字など不正値の場合の例外
def test_TC10_create_ticket_invalid_title(mocker):
    TicketService = mocker.Mock()
    # create_ticketで空文字タイトルの場合
    TicketService.create_ticket.side_effect = ValueError("Title cannot be empty")
    from target import test_change_status_follows_allowed_path
    with pytest.raises(ValueError):
        test_change_status_follows_allowed_path(TicketService)