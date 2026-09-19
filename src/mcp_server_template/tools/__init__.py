"""Tool capabilities exposed by the server."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from mcp_server_template.tools.example_tool import register_example_tools


def register_tools(server: MCPServer) -> None:
    """Attach every tool to ``server``. Add new modules and call them here."""
    register_example_tools(server)
