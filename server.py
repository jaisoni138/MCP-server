import pandas as pd
from pathlib import Path
from fastmcp import FastMCP, Context

# Initialize FastMCP server
mcp = FastMCP(name="mcp-custom-server")

# File path configuration
EXCEL_FILE = Path.home() / "Downloads" / "Jay_Estimated_cost_Future_plan.xlsx"

@mcp.tool()
def read_excel_data(ctx: Context, sheet_name: str = "Total Monthly expense") -> str:
    """
    Reads data from a local Excel file on Mac.
    Returns the data as a Markdown table for the LLM to process.
    """
    try:
        # Check if file exists
        if not EXCEL_FILE.exists():
            error_message = f"Excel file not found at: {EXCEL_FILE}"
            if ctx:
                ctx.error(error_message)
            return error_message

        # Read the Excel sheet
        # Note: Ensure 'openpyxl' is installed (pip install openpyxl)
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
        
        # Handle empty files or sheets
        if df.empty:
            return "The requested sheet is empty."

        # Convert to Markdown so the LLM can interpret the table structure
        return df.to_markdown(index=False)
        
    except Exception as e:
        error_msg = f"Failed to read Excel: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return error_msg

if __name__ == "__main__":
    mcp.run()
