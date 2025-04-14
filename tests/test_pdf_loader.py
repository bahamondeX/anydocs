"""Tests for PDF loader using URL sources."""

from anydocs import load_document

def test_pdf_loader_with_real_file():
    """Test the PDF loader with a real PDF file from URL."""
    url = "https://uneweb.edu.ve/tuto-docs/libro-python.pdf"
    
    try:
        # Load directly from URL
        content = list(load_document(url))
        
        # Check that content was extracted
        assert content, "No content was extracted from the PDF URL"
        
        # Check for Python references (it's a Python book)
        python_references_found = False
        for chunk in content:
            if "Python" in chunk or "python" in chunk:
                python_references_found = True
                break
        
        assert python_references_found, "No Python references found in the Python book"
    except Exception as e:
        # If there's a network error, we'll report but not fail
        raise e

def test_pdf_load_document():
    """Test loading a PDF file using the top-level load_document function."""
    url = "https://uneweb.edu.ve/tuto-docs/libro-python.pdf"
    
    try:
        # Load from URL
        content = list(load_document(url))
        
        # Check that content was extracted
        assert content, "No content was extracted using load_document"
        
        # Verify substantial content
        assert any(len(chunk) > 100 for chunk in content), "No substantial content found in PDF"
    except Exception as e:
        # If there's a network error, we'll report but not fail
        raise e

def test_pdf_text_extraction():
    """Test extracting plain text from a PDF URL."""
    url = "https://uneweb.edu.ve/tuto-docs/libro-python.pdf"
    
    try:
        # Test with text-only extraction
        content = list(load_document(url, extract_text_only=True))
        
        # Check that content was extracted
        assert content, "No content was extracted in text-only mode"
        
        # In text-only mode, we should have reasonable text
        has_substantial_text = False
        for chunk in content:
            if len(chunk) > 50:
                has_substantial_text = True
                break
                
        assert has_substantial_text, "No substantial text found in text-only mode"
    except Exception as e:
        # If there's a network error, we'll report but not fail
        raise e