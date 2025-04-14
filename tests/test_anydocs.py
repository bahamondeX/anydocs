"""Tests for the AnyDocs class using URL-based sources."""
from anydocs import load_document


def test_anydocs_with_url_sources():
    """Test that AnyDocs can handle URL sources directly."""
    # We'll test with a few URLs that should be relatively stable
    test_urls = [
        "https://raw.githubusercontent.com/bahamondeX/anytools/refs/heads/main/README.md",
        "https://wordpress.com/sitemap.xml",
    ]
    
    for url in test_urls:
        try:
            # Test with the load_document function
            content = list(load_document(url))
            
            # Check that content was extracted
            assert content, f"No content was extracted from URL: {url}"
            
            # URL parsing should work and extract content
            assert any(len(chunk) > 50 for chunk in content), f"No substantial content from URL: {url}"
        except Exception as e:
            # If there's a network error, we'll skip this test
            raise e