"""Entry point for the MCP server.

Builds an ``MCPServer`` instance (the v2 SDK replacement for ``FastMCP``) and
attaches every capability registered under ``tools/``, ``resources/`` and
``prompts/``.
"""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from mcp_server_template.prompts import register_prompts
from mcp_server_template.resources import register_resources
from mcp_server_template.tools import register_tools

SERVER_NAME = "mcp-template"


def create_server() -> MCPServer:
    """Assemble and return a fully configured :class:`MCPServer`."""
    server = MCPServer(
        name=SERVER_NAME,
        instructions=(
            "A starter MCP server template. Replace the example tools, "
            "resources and prompts with your own business logic."
        ),
        version="0.1.0",
    )
    register_tools(server)
    register_resources(server)
    register_prompts(server)
    return server


def main() -> None:
    """Run the server over stdio (the default local-client transport)."""
    create_server().run(transport="stdio")


if __name__ == "__main__":
    main()
