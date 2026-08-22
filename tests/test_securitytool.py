from securitytool import run_tool


def test_invalid_tool_selection():
    assert run_tool("99") is False


def test_empty_tool_selection():
    assert run_tool("") is False