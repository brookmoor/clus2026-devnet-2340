# DEVNET-2340 — Audience Reference

## Cisco Telemetry Broker (CTB)

**What it is:** Software broker that receives, replicates, and forwards network telemetry (NetFlow/IPFIX, sFlow, syslog) to multiple destinations without impacting sources.

| Resource | Link |
|----------|------|
| CTB Documentation | https://www.atomicmole.com/ctb-docs/ |
| CTB REST API Reference | [../docs/](../docs/) |
| Cisco Telemetry Broker | https://cs.co/telemetrybroker |

---

## Model Context Protocol (MCP)

**What it is:** Open standard for connecting AI assistants to external tools and data sources. Defines how AI models discover and call tools safely.

| Resource | Link |
|----------|------|
| MCP Specification | https://modelcontextprotocol.io |
| MCP GitHub | https://github.com/modelcontextprotocol |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| MCP Server Examples | https://github.com/modelcontextprotocol/servers |
| Building MCP Servers (Tutorial) | https://modelcontextprotocol.io/quickstart/server |

---

## Claude Code

**What it is:** Anthropic's AI coding assistant with native MCP support, available as CLI, desktop app, and IDE extension.

| Resource | Link |
|----------|------|
| Claude Code | https://claude.ai/code |
| Claude Code Docs | https://docs.anthropic.com/en/docs/claude-code |
| Claude Code GitHub | https://github.com/anthropics/claude-code |

---

## APIs & Tools Used in This Demo

| Tool | Purpose |
|------|---------|
| CTB REST API (`/api-v1/`) | Manage inputs, outputs, subscriptions |
| MCP (stdio transport) | Connect Claude to CTB API securely |
| Docker | Run MCP server as containerized service |
| curl + python3 | Quick API scripting demos |

---

## Architecture (What We Showed)

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│  Telemetry  │────▶│ CTB Broker  │────▶│  Collectors  │
│  Sources    │     │ (VPP-based) │     │  (Splunk,    │
│  (NetFlow)  │     │             │     │   SIEM, etc) │
└─────────────┘     └──────┬──────┘     └──────────────┘
                           │
                    ┌──────┴──────┐
                    │ CTB Manager │◀──── REST API
                    │  (Control)  │         │
                    └─────────────┘         │
                                      ┌────┴────┐
                                      │   MCP   │
                                      │ Server  │
                                      └────┬────┘
                                           │
                                      ┌────┴────┐
                                      │  Claude │
                                      │  Code   │
                                      └─────────┘
```

---

## Session Info

**DEVNET-2340** — Cisco Telemetry Broker: From UI to API to AI
Cisco Live US 2026

---

*Scan for this page:*

`[QR CODE PLACEHOLDER — generate at https://qr.io or similar pointing to a short URL with this content]`

Suggested short URL: Create a bit.ly or cisco.com/go/ link pointing to either:
- A GitHub gist with this content
- The CTB DevNet page
- A landing page you create with all links
