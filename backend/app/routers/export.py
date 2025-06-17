"""
Export API endpoints for SMARTNEED
"""

from fastapi import APIRouter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/sheets")
async def export_to_sheets(data: dict):
    """Export data to Google Sheets"""
    logger.info(f"Mock export to sheets: {data}")
    return {
        "message": "Data exported successfully (mock)",
        "sheet_url": "https://docs.google.com/spreadsheets/mock_sheet_id",
        "rows_exported": len(data.get("products", []))
    }
