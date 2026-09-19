"""Example prompts. Copy this module as a blueprint for real prompts."""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer


def register_example_prompts(server: MCPServer) -> None:
    """Register the demo prompts onto ``server``."""

    @server.prompt()
    def analyze_code(code: str, language: str = "python") -> str:
        """Prompt asking the model to review a snippet of code."""
        return f"Please review the following {language} code:\n\n{code}"
