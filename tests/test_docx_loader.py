"""Tests for DOCX loader using real-world files."""

import pytest
from pathlib import Path

from anydocs import DocxLoader, load_document
from tests.conftest import get_test_file_path


def test_docx_loader_with_real_file():
    """Test the DOCX loader with a real DOCX file from calibre-ebook."""
    file_path = get_test_file_path("demo.docx")
    
    # Test direct loader usage
    loader = DocxLoader(ref=str(file_path))
    content = list(loader.extract())
    
    # Check that content was extracted
    assert content, "No content was extracted from the DOCX file"
    
    # The demo.docx file should contain text content
    text_chunks_found = False
    for chunk in content:
        if chunk.startswith("<p>") and len(chunk) > 10:
            text_chunks_found = True
            break
    
    assert text_chunks_found, "No text chunks found in extracted content"
    
    # Check for document properties (title, author if available)
    doc_properties_found = False
    for chunk in content[:5]:  # Check first few chunks where properties usually appear
        if "<h1>" in chunk or "<p><strong>Author:" in chunk:
            doc_properties_found = True
            break
    
    # Note: Not all documents have properties, so this is not a strict assertion
    if not doc_properties_found:
        print("Warning: No document properties found in the DOCX file")


def test_docx_load_document():
    """Test loading a DOCX file using the top-level load_document function."""
    file_path = get_test_file_path("demo.docx")
    
    # Test with the load_document function
    content = list(load_document(str(file_path)))
    
    # Check that content was extracted
    assert content, "No content was extracted using load_document"
    
    # Look for paragraphs in the content
    paragraphs_found = False
    for chunk in content:
        if "<p>" in chunk and "</p>" in chunk:
            paragraphs_found = True
            break
    
    assert paragraphs_found, "No paragraphs found in extracted content"


def test_docx_text_extraction():
    """Test extracting plain text from a DOCX file."""
    file_path = get_test_file_path("demo.docx")
    
    # Test with the load_document function and text_only=True
    content = list(load_document(str(file_path), extract_text_only=True))
    
    # Check that content was extracted
    assert content, "No content was extracted in text-only mode"
    
    # In text-only mode, we should have no HTML tags
    for chunk in content:
        assert "<p>" not in chunk, "HTML tags found in text-only extraction"
        assert "</p>" not in chunk, "HTML tags found in text-only extraction"
        
    # Check that the text content has reasonable length
    total_text = "".join(content)
    assert len(total_text) > 50, "Text content is suspiciously short"