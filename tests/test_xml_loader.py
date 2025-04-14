"""Tests for XML loader using URL-based tests."""

import json
from anydocs import load_document

# This test file will test XML loading functionality with URLs rather than mock data
def test_xml_with_url():
    """Test loading XML from a URL."""
    # Test directly with the WordPress sitemap URL
    url = "https://wordpress.com/sitemap.xml"
    
    try:
        # Load the XML from the URL
        content = list(load_document(url))
        
        # Verify we got some content
        assert content, "No content extracted from sitemap.xml URL"
    except Exception as e:
        # If there's a network error, we'll report but not fail
        raise e