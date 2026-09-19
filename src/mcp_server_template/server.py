"""Entry point for the MCP server.

Builds an ``MCPServer`` instance (the v2 SDK replacement for ``FastMCP``) and
attaches every capability registered under ``tools/``, ``resources/`` and
``prompts/``.

Transports
----------
* ``stdio`` (default) — the client (VS Code, Claude Desktop, ...) spawns this
  process and talks to it over stdin/stdout. No manual start needed: the
  client owns the process lifecycle (one process per client session).
* ``streamable-http`` / ``sse`` — long-running HTTP server. Start it yourself
  (or via the VS Code task / Windows Task Scheduler) and connect a remote
  client to ``http://<host>:<port>/mcp`` (or ``/sse``).
"""

from __future__ import annotations

import argparse

from mcp.server.mcpserver import MCPServer

from mcp_server_template.prompts import register_prompts
from mcp_server_template.resources import register_resources
from mcp_server_template.tools import register_tools

SERVER_NAME = "mcp-template"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the command-line arguments.

    ``argv`` is injectable so tests can exercise the parser without touching
    ``sys.argv``.
    """
    parser = argparse.ArgumentParser(
        prog="mcp-server-template",
        description="MCP server template (mcp SDK v2).",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport to run over. 'stdio' is managed by the client; the "
        "HTTP transports start a long-running server (default: stdio).",
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Bind address for HTTP transports (default: {DEFAULT_HOST}).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Bind port for HTTP transports (default: {DEFAULT_PORT}).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Run the server using the selected transport.

    ``stdio`` needs no extra options; ``sse`` and ``streamable-http`` accept
    ``host`` / ``port`` (forwarded as transport kwargs by the SDK).
    """
    args = parse_args(argv)
    server = create_server()
    if args.transport == "stdio":
        server.run(transport="stdio")
    else:
        server.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
