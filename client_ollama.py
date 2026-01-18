# client_ollama.py
from fastmcp import Client as MCPClient

MCP_SERVER_URL = "http://127.0.0.1:8080/sse"

async def query_ollama(prompt: str):
    async with MCPClient(MCP_SERVER_URL) as mcp:
        # Auto-detect Ollama chat tool
        tools = await mcp.list_tools()
        tool_name = None
        for t in tools:
            if "llama" in t.name.lower() or "chat" in t.name.lower():
                tool_name = t.name
                break
        if not tool_name:
            return "❌ No Ollama chat tool found"

        # Call the tool
        result = await mcp.call_tool(tool_name, {"prompt": prompt})

        # Extract text
        if hasattr(result, "content") and result.content:
            texts = []
            for item in result.content:
                if hasattr(item, "text"):
                    texts.append(item.text)
                elif hasattr(item, "data"):
                    texts.append(str(item.data))
            return "\n".join(texts) if texts else "⚠️ Ollama returned empty content"
        elif hasattr(result, "text"):
            return str(result.text)
        elif isinstance(result, str):
            return result
        else:
            return str(result)
