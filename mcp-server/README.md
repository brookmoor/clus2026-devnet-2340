# CTB Manager MCP Server

MCP (Model Context Protocol) server that exposes CTB Manager REST API operations to AI assistants like Claude.

## What is MCP?

MCP is an open standard for connecting AI assistants to external tools and data sources. This server lets Claude (or any MCP-compatible AI) directly manage CTB — listing nodes, creating inputs/outputs, and wiring subscriptions.

## Setup

1. Copy `.env.example` to `.env` and configure credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your CTB Manager IP and credentials
   ```

2. Build and start the server:
   ```bash
   docker-compose up -d
   ```

3. Configure Claude Code to use the MCP server. Add to your `~/.claude/settings.json`:
   ```json
   {
     "mcpServers": {
       "ctb-manager": {
         "command": "docker",
         "args": ["run", "--rm", "-i",
           "-e", "CTB_MANAGER_IP=<your-manager-ip>",
           "-e", "CTB_USERNAME=admin",
           "-e", "CTB_PASSWORD=<your-password>",
           "ctb-mcp"]
       }
     }
   }
   ```

## Available Tools

| Tool | Description |
|------|-------------|
| `ctb_get_nodes` | List broker nodes |
| `ctb_get_input_types` | Get supported input types |
| `ctb_get_inputs` | List inputs (optionally by ID) |
| `ctb_get_outputs` | List outputs (optionally by ID) |
| `ctb_get_subscriptions` | List all subscriptions |
| `ctb_create_input` | Create a new UDP input on a broker |
| `ctb_create_output` | Create a new UDP output destination |
| `ctb_create_subscription` | Link an input to an output |

## Architecture

```
┌──────────┐    stdio/SSE     ┌───────────┐    HTTPS    ┌─────────────┐
│  Claude  │ ◄──────────────► │ MCP Server│ ◄─────────► │ CTB Manager │
│  Code    │                  │ (Python)  │             │  REST API   │
└──────────┘                  └───────────┘             └─────────────┘
```

The server handles authentication, CSRF tokens, and session management transparently.

## Development

```bash
pip install -e ".[dev]"
python -m ctb_mcp          # stdio mode (for Claude Code)
python -m ctb_mcp --sse    # HTTP/SSE mode (port 8000)
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CTB_MANAGER_IP` | CTB Manager hostname or IP |
| `CTB_USERNAME` | Admin username |
| `CTB_PASSWORD` | Admin password |
