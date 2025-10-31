from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import requests

# Create a vulnerable MCP server for Demo 1 - Intro to Prompt Injection
mcp = FastMCP("Demo 1 - Intro to Prompt Injection")

# A Sample make HTTP request method just for the demo
@mcp.tool()
async def sendinfo(loc: str) -> str:
    """Send GET HTTP request

    Args:
        Url
    """
    # vulnerable method as now URL whitelist approch implemented here
    r = requests.get(loc,verify=False)
    return 'Request sent successfully.'

# Add a tool that provides user information
@mcp.tool()
async def get_user_info(username: str) -> str:
    """Get notes information about user

    Args:
        username
    """
    # Simulate a user database
    users = {
        "user1": "Regular user with basic access",
        "user2": "Project manager with elevated access",
        "admin": "System administrator with full access"
    }
    
    if username in users:
        return f"User information for {username}: {users[username]}"
    else:
        return f"User not found: {username}"

def main():
    print("[ + ] Simple MCP Server running locally...")
    # Run stdio transport for local testing / CTF-style usage
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()