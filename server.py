from pathlib import Path
from fastmcp import FastMCP, Context

mcp = FastMCP(name="mcp-custom-server")

DATA_PATH = Path(__file__).parent / "data" / "data.txt"


@mcp.tool()
def get_custom_data(ctx: Context) -> str:
    """
    Retrieves information about Breaking News from a local file. In real world scenario we would fetch data from
    external api or local database. We could also build a custom RAG pipeline and expose it through our MCP server.
    """
    try:
        info_text = DATA_PATH.read_text()
        return info_text
    except FileNotFoundError:
        error_message = f"Error: The file '{DATA_PATH}' was not found."
        ctx.error(error_message)
        return "Information not available."


if __name__ == "__main__":
    mcp.run()
