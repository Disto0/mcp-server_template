Write your own MCP Tool in python.

# MCP Server Template (Python)

A minimal, opinionated starter template for building [Model Context Protocol](https://modelcontextprotocol.io/) servers in Python using the official `mcp` SDK (**v2**, where `FastMCP` is now `MCPServer`).

Built and managed with [`uv`](https://docs.astral.sh/uv/).

## Requirements

- Python >= 3.14
- `uv` installed

> **Note on the SDK version:** this template targets `mcp>=2,<3`. In v2,
> `FastMCP` was renamed to `MCPServer` and imported from
> `mcp.server.mcpserver`. If you need the older API, pin `mcp<2`.

## Quick start

```bash
uv sync          # install dependencies + this package (editable)
uv run pytest    # run the test suite
uv run mcp-server-template   # start the server over stdio
```

## Project layout

```text
src/mcp_server_template/
├── __init__.py            # package version
├── server.py              # builds the MCPServer, registers capabilities
├── tools/                 # tool handlers (business logic)
│   ├── __init__.py        # register_tools(server) aggregator
│   └── example_tool.py    # echo / add demo tools
├── resources/             # resource handlers
│   ├── __init__.py        # register_resources(server) aggregator
│   └── example_resource.py
└── prompts/               # prompt handlers
    ├── __init__.py        # register_prompts(server) aggregator
    └── example_prompt.py
tests/
└── test_server.py         # verifies capabilities are registered & callable
```

## How to add a capability

1. Create a module under `tools/` (or `resources/`, `prompts/`).
2. Define a `register_*(server)` function that uses the decorators
   `@server.tool()`, `@server.resource("uri")` or `@server.prompt()`.
3. Call your `register_*` function from the matching package `__init__.py`.

The docstring of each handler becomes its description, and type hints define
the argument schema automatically.

## Connecting a client (Claude Desktop / Cursor)

Add an entry to your client's MCP config. Use an **absolute** path to this
project directory:

```json
{
  "mcpServers": {
    "mcp-template": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/MCP_Server_Template",
        "run",
        "mcp-server-template"
      ]
    }
  }
}
```

(Continue)
```yaml
mcpServers:
  - name: mcp-template
    command: uv
    args:
      - --directory
      - "ABSOLUTE\\PATH\\TO\\mcp-server_template"
      - run
      - mcp-server-template
```

## Environment variables

If your tools need secrets, read them from the environment (e.g. `os.environ`)
and provide them via your client's `env` block or a local `.env` file you load
yourself. Never commit real secrets.

## Server lifecycle & automation

### stdio (default): the client manages the server

With the **stdio** transport you never start the server manually. The client
(VS Code, Claude Desktop, ...) spawns the process itself using the config
above, talks to it over stdin/stdout, and **kills it when the session ends**.
Each client session gets its own process — that is normal and intended.

### HTTP transports: a long-running process

`streamable-http` (and `sse`) run a persistent HTTP server. Start it once and
connect any remote client to the endpoint:

```bash
uv run mcp-server-template --transport streamable-http --host 127.0.0.1 --port 8000
# endpoint: http://127.0.0.1:8000/mcp
```

CLI options: `--transport {stdio,sse,streamable-http}`, `--host`, `--port`.

#### Automation options

| Context | How |
|---|---|
| **VS Code** | `.vscode/tasks.json` ships two tasks: `MCP: Start Server (stdio)` and `MCP: Start Server (streamable-http)`. The HTTP task has `runOnFolderOpen: true`, so it starts automatically when you open the folder. Run it manually via *Terminal → Run Task*. |
| **Windows (logon)** | `scripts/setup-windows-task.ps1` registers a **Task Scheduler** task that starts the HTTP server at user logon, with automatic restart (3×) on failure. See below. |
| **Windows (service)** | For a service that survives logout, wrap it with [NSSM](https://nssm.cc/): `nssm install mcp-server-template <path-to-uv> run mcp-server-template --transport streamable-http` |
| **Docker / Linux** | Standard container or `systemd` unit running the same command. |

#### Windows Task Scheduler (one-liner)

```powershell
# Create (idempotent — re-running updates the task):
pwsh scripts/setup-windows-task.ps1

# Custom port:
pwsh scripts/setup-windows-task.ps1 -Port 9000

# Remove:
pwsh scripts/setup-windows-task.ps1 -Remove
```

The script resolves `uv` from PATH and pins the working directory to the
project root, so the task keeps working after the folder is moved.
