"""Tests for Excel (XLSX) loader using URL-based files."""

from anydocs import load_document

def test_xlsx_loader_with_url():
    """Test the XLSX loader with a direct URL."""
    # Use URL directly
    url = "https://raw.githubusercontent.com/frictionlessdata/datasets/main/files/excel/sample-1-sheet.xlsx"
    
    try:
        # Load the document
        content = list(load_document(url))
        
        # Check that content was extracted
        assert content, "No content was extracted from the XLSX URL"

    except Exception as e:
        # If there's a network error, we'll report but not fail
        raise e