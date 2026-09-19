"""Example resources. Copy this module as a blueprint for real resources."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer


def register_example_resources(server: MCPServer) -> None:
    """Register the demo resources onto ``server``."""

    @server.resource("about://server")
    async def about() -> str:
        """A static resource describing the server."""
        return "This is the mcp-server-template starter server."

    @server.resource("user://{name}")
    async def user_profile(name: str) -> str:
        """A dynamic resource template resolved per user name."""
        return f"Profile for {name}"
