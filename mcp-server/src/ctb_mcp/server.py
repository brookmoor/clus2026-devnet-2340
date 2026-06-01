"""MCP server exposing CTB Manager operations."""
import asyncio
import json
import logging
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.routing import Route
from .session import create_session_from_env, CTBSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global session instance
ctb_session: CTBSession = None

# Create MCP server
app = Server("ctb-manager")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available CTB Manager tools."""
    return [
        Tool(
            name="ctb_get_nodes",
            description="Retrieve broker nodes available in CTB Manager",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="ctb_get_input_types",
            description="Retrieve supported input types for CTB Manager",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="ctb_get_inputs",
            description="Retrieve inputs from CTB Manager, optionally filtered by input ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_id": {
                        "type": "string",
                        "description": "Optional input ID to retrieve specific input",
                    }
                },
            },
        ),
        Tool(
            name="ctb_get_outputs",
            description="Retrieve outputs (destinations) from CTB Manager, optionally filtered by output ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_id": {
                        "type": "string",
                        "description": "Optional output ID to retrieve specific output",
                    }
                },
            },
        ),
        Tool(
            name="ctb_get_subscriptions",
            description="Retrieve all subscriptions (input-to-output mappings) from CTB Manager",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="ctb_create_input",
            description="Create a new telemetry input on a broker node. Listens for incoming telemetry on the specified UDP port.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Display name for the input",
                    },
                    "node": {
                        "type": "integer",
                        "description": "Broker node ID to create the input on",
                    },
                    "port": {
                        "type": "integer",
                        "description": "UDP port to listen on for incoming telemetry",
                    },
                    "input_type": {
                        "type": "string",
                        "description": "Input type (default: udp_listener)",
                        "default": "udp_listener",
                    },
                },
                "required": ["name", "node", "port"],
            },
        ),
        Tool(
            name="ctb_create_output",
            description="Create a new telemetry output (destination) on a broker node. Forwards telemetry to the specified IP and port.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Display name for the output",
                    },
                    "node": {
                        "type": "integer",
                        "description": "Broker node ID to create the output on",
                    },
                    "address": {
                        "type": "string",
                        "description": "Destination IP address to forward telemetry to",
                    },
                    "port": {
                        "type": "integer",
                        "description": "Destination UDP port",
                    },
                    "output_type": {
                        "type": "string",
                        "description": "Output type (default: udp)",
                        "default": "udp",
                    },
                },
                "required": ["name", "node", "address", "port"],
            },
        ),
        Tool(
            name="ctb_create_subscription",
            description="Create a subscription that maps an input to an output, causing telemetry received on the input to be forwarded to the output.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "integer",
                        "description": "Input ID (source of telemetry)",
                    },
                    "destination": {
                        "type": "integer",
                        "description": "Output ID (destination for telemetry)",
                    },
                    "subnets": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of subnet filters (empty means all traffic)",
                        "default": [],
                    },
                },
                "required": ["source", "destination"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    global ctb_session

    try:
        if name == "ctb_get_nodes":
            response = await asyncio.to_thread(ctb_session.get_nodes)
            response.raise_for_status()
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

        elif name == "ctb_get_input_types":
            response = await asyncio.to_thread(ctb_session.get_input_types)
            response.raise_for_status()
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

        elif name == "ctb_get_inputs":
            input_id = arguments.get("input_id")
            response = await asyncio.to_thread(ctb_session.get_inputs, input_id)
            response.raise_for_status()
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

        elif name == "ctb_get_outputs":
            output_id = arguments.get("output_id")
            response = await asyncio.to_thread(ctb_session.get_outputs, output_id)
            response.raise_for_status()
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

        elif name == "ctb_get_subscriptions":
            response = await asyncio.to_thread(ctb_session.get_subscriptions)
            response.raise_for_status()
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

        elif name == "ctb_create_input":
            response = await asyncio.to_thread(
                ctb_session.create_input,
                name=arguments["name"],
                node=arguments["node"],
                port=arguments["port"],
                input_type=arguments.get("input_type", "udp_listener"),
            )
            response.raise_for_status()
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

        elif name == "ctb_create_output":
            response = await asyncio.to_thread(
                ctb_session.create_output,
                name=arguments["name"],
                node=arguments["node"],
                address=arguments["address"],
                port=arguments["port"],
                output_type=arguments.get("output_type", "udp"),
            )
            response.raise_for_status()
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

        elif name == "ctb_create_subscription":
            response = await asyncio.to_thread(
                ctb_session.create_subscription,
                source=arguments["source"],
                destination=arguments["destination"],
                subnets=arguments.get("subnets", []),
            )
            response.raise_for_status()
            return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error executing {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_sse(request):
    """Handle SSE endpoint for MCP communication."""
    async with SseServerTransport("/messages") as transport:
        await app.run(
            transport.read_stream,
            transport.write_stream,
            app.create_initialization_options()
        )


async def run_stdio():
    """Run the MCP server with stdio transport (for Claude Code)."""
    global ctb_session

    logger.info("Initializing CTB Manager session...")
    try:
        ctb_session = create_session_from_env()
        logger.info("Successfully authenticated to CTB Manager")
    except Exception as e:
        logger.error(f"Failed to initialize CTB session: {e}")
        raise

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


async def run_sse():
    """Run the MCP server with HTTP/SSE transport."""
    global ctb_session

    logger.info("Initializing CTB Manager session...")
    try:
        ctb_session = create_session_from_env()
        logger.info("Successfully authenticated to CTB Manager")
    except Exception as e:
        logger.error(f"Failed to initialize CTB session: {e}")
        raise

    starlette_app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse)
        ]
    )

    import uvicorn
    logger.info("Starting MCP server on http://0.0.0.0:8000")
    config = uvicorn.Config(starlette_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """Run server in stdio mode (default) or SSE mode with --sse flag."""
    if "--sse" in sys.argv:
        await run_sse()
    else:
        await run_stdio()


if __name__ == "__main__":
    asyncio.run(main())
