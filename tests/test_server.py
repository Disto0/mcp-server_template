"""Tests for the MCP server assembly and capabilities."""

import asyncio

from mcp_server_template.server import create_server


def test_create_server_registers_capabilities():
    server = create_server()
    tools = asyncio.run(server.list_tools())
    prompts = asyncio.run(server.list_prompts())
    resources = asyncio.run(server.list_resources())

    tool_names = {t.name for t in tools}
    assert {"echo", "add"}.issubset(tool_names)
    assert len(prompts) >= 1
    assert len(resources) >= 1


def test_add_tool_returns_sum():
    server = create_server()
    result = asyncio.run(server.call_tool("add", {"a": 2, "b": 3}))
    # call_tool returns a CallToolResult; the structured payload holds the value.
    assert result.structured_content["result"] == 5
