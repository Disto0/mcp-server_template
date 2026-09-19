"""Prompt capabilities exposed by the server."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from mcp_server_template.prompts.example_prompt import register_example_prompts


def register_prompts(server: MCPServer) -> None:
    """Attach every prompt to ``server``."""
    register_example_prompts(server)
