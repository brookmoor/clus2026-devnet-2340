"""Entry point for running ctb-mcp as a module."""
import asyncio
from .server import main

asyncio.run(main())
