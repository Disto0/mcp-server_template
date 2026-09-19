"""Tests for the MCP server assembly and capabilities."""

import asyncio

from mcp_server_template.server import create_server, parse_args


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


def test_parse_args_defaults_to_stdio():
    args = parse_args([])
    assert args.transport == "stdio"
    assert args.host == "127.0.0.1"
    assert args.port == 8000


def test_parse_args_http_transport():
    args = parse_args(
        ["--transport", "streamable-http", "--host", "0.0.0.0", "--port", "9000"]
    )
    assert args.transport == "streamable-http"
    assert args.host == "0.0.0.0"
    assert args.port == 9000
