import pandas as pd
from pathlib import Path
from fastmcp import FastMCP, Context

mcp = FastMCP(name="mac-excel-server")

# Pro-tip: Use home-relative paths for Mac portability
EXCEL_FILE = Path.home() / "Downloads" / "Jay_Estimated_cost_Future_plan.xlsx"

@mcp.tool()
def read_excel_data(sheet_name: str = "Total Monthly expense", ctx: Context) -> str:
    """
    Reads data from a local Excel file on Mac.
    Returns the data as a Markdown table for the LLM to process.
    """
    try:
        # Check if file exists before processing
        if not EXCEL_FILE.exists():
            raise FileNotFoundError(f"Excel file not found at {EXCEL_FILE}")

        # Read the Excel sheet
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
        
        # Convert to Markdown so the LLM can "see" the table structure
        return df.to_markdown(index=False)
        
    except Exception as e:
        error_msg = f"Failed to read Excel: {str(e)}"
        ctx.error(error_msg)
        return error_msg

if __name__ == "__main__":
    mcp.run()
