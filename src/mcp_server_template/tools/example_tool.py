"""Example tools. Copy this module as a blueprint for real tools."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer


def register_example_tools(server: MCPServer) -> None:
    """Register the demo tools onto ``server``."""

    @server.tool()
    async def echo(text: str) -> str:
        """Return the input text unchanged. Useful to verify the server works."""
        return text

    @server.tool()
    async def add(a: float, b: float) -> float:
        """Add two numbers and return the result."""
        return a + b
