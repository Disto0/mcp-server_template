"""Resource capabilities exposed by the server."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from mcp_server_template.resources.example_resource import (
    register_example_resources,
)


def register_resources(server: MCPServer) -> None:
    """Attach every resource to ``server``."""
    register_example_resources(server)
