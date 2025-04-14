"""Tests for CSV loader using URL-based files."""

import json

from anydocs import load_document

def test_csv_loader_with_real_data():
    """Test the CSV loader with a real CSV file from plotly datasets."""
    # Use URL directly
    url = "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/data.csv"
    
    try:
        # Load document from URL
        content = list(load_document(url))
        
        # Check that content was extracted
        assert content, "No content was extracted from the CSV file"
        
        # At least one chunk should contain data
        data_found = False
        for chunk in content:
            if "data" in chunk.lower():
                data_found = True
                break
                
        assert data_found, "No data found in CSV content"
    except Exception as e:
        # If there's a network error, we'll report but not fail
        raise e