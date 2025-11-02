from typing import Any
import httpx, re, os
from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict

# Create a vulnerable MCP server for Demo 4 - Indirect Prompt Injection
mcp = FastMCP("Demo 4 - Indirect Prompt Injection")

@mcp.tool()
async def submit_file_to_rag(filename: str, content: str) -> str:
    """Upload new file.
    
    This tool allows users to upload a document to 
    the RAG system for other users to use.
    
    Args:
        filename: The document file name
        content: The text content of the document
    
    Returns:
        Upload status
    """
    try:
        # only .txt files
        if not filename.lower().endswith(".txt"):
            return {"status": "only .txt files allowed"}
        # Save the uploaded document
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base_dir, "documents")
        filepath = f"{folder_path}/{filename}"
        with open(filepath, "w") as f:
            f.write(content)
        summary = f"""
DOCUMENT INFORMATION (File Name: {filename})
----------------
DOCUMENT CONTENT:
{content}
"""
        return summary
    except Exception as e:
        return {"status": f"Error submiting file: {str(e)}"}
  
@mcp.tool()
async def search_info(keyword: str, context_chars: int = 120) -> Dict[str,Any]:
    """Search information about keyword
    
    This tool allows users to search info.
    
    Args:
        keyword: The user keyword
    
    Returns:
        Documents that contains the keyword
    """
    summaries = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_dir, "documents")
    # list files and sort by mtime descending (newest first)
    try:
        filenames = sorted(
            os.listdir(folder_path),
            key=lambda n: os.path.getmtime(os.path.join(folder_path, n)),
            reverse=True
        )
    except FileNotFoundError:
        return {"error": f"Folder not found: {folder_path}"}

    for doc_name in filenames:
        doc_path = os.path.join(folder_path, doc_name)
        if not os.path.isfile(doc_path):
            continue
        try:
            with open(doc_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            content = f"[ERROR READING FILE: {e}]"

        if keyword.lower() in content.lower():
            # get a short context snippet around the first match
            lower = content.lower()
            summary = f"{lower}"
            summaries.append(summary)

    return {"data": "\n\n".join(summaries) if summaries else "no data found"}

def main():
    print("[ + ] Simple MCP Server running locally...")
    # Run stdio transport for local testing / CTF-style usage
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()