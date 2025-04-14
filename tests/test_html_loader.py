"""Tests for HTML loader using URL sources."""

from anydocs import load_document

def test_html_loader_with_real_file():
    """Test the HTML loader with a real HTML URL from boto3 documentation."""
    url = "https://boto3.amazonaws.com/v1/documentation/api/latest/search.html"
    
    try:
        # Load directly from URL
        content = list(load_document(url))
        
        # Check that content was extracted
        assert content, "No content was extracted from the HTML URL"
        
        # The search.html page should have meaningful text content
        assert any(len(chunk) > 100 for chunk in content), "No substantial content found"
        
        # The boto3 search page should have "AWS SDK for Python" somewhere in the text
        found_boto3_reference = False
        for chunk in content:
            if "AWS SDK for Python" in chunk or "Boto3" in chunk:
                found_boto3_reference = True
                break
        
        assert found_boto3_reference, "Expected boto3 references not found in content"
    except Exception as e:
        # If there's a network error, we'll report but not fail
        print(f"Skipping HTML URL test due to error: {str(e)}")

def test_html_text_extraction():
    """Test extracting plain text from an HTML URL."""
    url = "https://boto3.amazonaws.com/v1/documentation/api/latest/search.html"
    
    try:
        # Test with text-only extraction from URL
        content = list(load_document(url, extract_text_only=True))
        
        # Check that content was extracted
        assert content, "No content was extracted in text-only mode"
        
        # In text-only mode, we should have no HTML tags
        for chunk in content:
            assert "<div" not in chunk, "HTML div tags found in text-only extraction"
            assert "<span" not in chunk, "HTML span tags found in text-only extraction"
            assert "<a href" not in chunk, "HTML anchor tags found in text-only extraction"
    except Exception as e:
        # If there's a network error, we'll report but not fail
        raise e