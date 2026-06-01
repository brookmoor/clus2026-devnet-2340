# Cisco Live US 2026

## Cisco Telemetry Broker: From UI to API to AI [DEVNET-2340]

This session demonstrates how Cisco Telemetry Broker (CTB) can be managed programmatically — from manual UI operations, to scripted API calls, to AI-driven automation using Model Context Protocol (MCP).

### What's in this repo

| Directory | Contents |
|-----------|----------|
| `api-examples/` | Shell scripts demonstrating CTB REST API operations |
| `mcp-server/` | MCP server that connects Claude to CTB Manager |
| `docs/` | CTB API reference and session resources |

### Demo Flow

1. **UI** — Manual input/output/subscription creation via CTB Manager web UI
2. **API** — Same operations scripted with curl (`api-examples/`)
3. **Bulk API** — Create 10 inputs, 10 outputs, 9 subscriptions in seconds
4. **AI + MCP** — Claude discovers a missing subscription and fixes it autonomously

### CTB API Quick Reference

Base URL: `https://<manager-ip>/api-v1/`

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List nodes | GET | `/nodes/` |
| List input types | GET | `/input-types/` |
| List inputs | GET | `/inputs/` |
| Create input | POST | `/inputs/` |
| Delete input | DELETE | `/inputs/<id>/` |
| List outputs | GET | `/outputs/` |
| Create output | POST | `/outputs/` |
| Delete output | DELETE | `/outputs/<id>/` |
| List subscriptions | GET | `/subscriptions/` |
| Create subscription | POST | `/subscriptions/` |
| Delete subscription | DELETE | `/subscriptions/<id>/` |

Authentication: HTTP Basic Auth (`-u admin:<password>`)

### Running the MCP Server

```bash
cd mcp-server
cp .env.example .env   # Edit with your CTB Manager credentials
docker-compose up -d
```

See [mcp-server/README.md](mcp-server/README.md) for full setup instructions.

### Resources

| Resource | Link |
|----------|------|
| CTB Documentation | https://www.cisco.com/go/ctb |
| CTB REST API Reference | https://developer.cisco.com/docs/cisco-telemetry-broker/ |
| CTB on DevNet | https://developer.cisco.com/cisco-telemetry-broker/ |
| MCP Specification | https://modelcontextprotocol.io |
| Claude Code | https://claude.ai/code |

### Session Info

**DEVNET-2340** — Cisco Telemetry Broker: From UI to API to AI
Cisco Live US 2026 | Presenter: Ajit Thyagarajan
