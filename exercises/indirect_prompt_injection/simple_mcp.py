from typing import Any
import httpx, re
from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict

# Create a vulnerable MCP server for Demo 4 - Indirect Prompt Injection
mcp = FastMCP("Demo 4 - Indirect Prompt Injection")

# Add a tool that summrize remote webpage content
@mcp.tool()
async def summrize(url: str) -> Dict[str, str]:
    """Summrize webpage content

    Args:
        url
    """
    # Simulate a fetch to remote URL
    rsource = requests.get(url,verify=False)
    return {"content": str(rsource.text)}

def main():
    print("[ + ] Simple MCP Server running locally...")
    # Run stdio transport for local testing / CTF-style usage
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()