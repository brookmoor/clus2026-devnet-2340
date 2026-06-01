FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install package
RUN pip install --no-cache-dir -e .

# Expose port for SSE
EXPOSE 8000

# Run MCP server
CMD ["python", "-m", "ctb_mcp"]
