


def test_yard_rule_status_loaded(yard_rule_status):
    """
    Purpose:
    --------
    Ensure yard rule configuration is reachable and structured.
    """

    assert "siteId" in yard_rule_status
    assert "isAutoPlan" in yard_rule_status
    assert "isOnly40on40And20on20" in yard_rule_status
    assert "isTabularOnYardView" in yard_rule_status
