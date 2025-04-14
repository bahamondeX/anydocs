"""Tests for Markdown loader using real-world files."""

import pytest
from pathlib import Path

from anydocs import MarkdownLoader, load_document
from tests.conftest import get_test_file_path


def test_markdown_loader_with_real_file():
    """Test the Markdown loader with a real MD file from GitHub."""
    file_path = get_test_file_path("README.md")
    
    # Test direct loader usage
    loader = MarkdownLoader(ref=str(file_path))
    content = list(loader.extract())
    
    # Check that content was extracted
    assert content, "No content was extracted from the Markdown file"
    
    # Check that Markdown was converted to HTML
    html_content_found = False
    for chunk in content:
        # Look for evidence of Markdown->HTML conversion like headers, paragraphs
        if ("<h1>" in chunk or "<h2>" in chunk or "<p>" in chunk or "<ul>" in chunk or 
            "<strong>" in chunk or "<em>" in chunk):
            html_content_found = True
            break
    
    assert html_content_found, "No HTML content found (Markdown conversion failed)"
    
    # Check for image processing
    if "![" in open(file_path, "r").read():
        # If the original MD has images, check if they were processed
        image_processing_attempted = False
        for chunk in content:
            if "<img" in chunk and "src=" in chunk:
                image_processing_attempted = True
                break
            
        assert image_processing_attempted, "Markdown images were not processed"


def test_markdown_load_document():
    """Test loading a Markdown file using the top-level load_document function."""
    file_path = get_test_file_path("README.md")
    
    # Test with the load_document function
    content = list(load_document(str(file_path)))
    
    # Check that content was extracted
    assert content, "No content was extracted using load_document"
    
    # Check that we got HTML content from the Markdown
    assert any("<h1>" in chunk or "<h2>" in chunk for chunk in content), "No HTML headers found"
    
    # README files typically have headers and descriptions
    total_content = "".join(content)
    assert len(total_content) > 100, "README content is suspiciously short"


def test_markdown_text_extraction():
    """Test extracting plain text from a Markdown file."""
    file_path = get_test_file_path("README.md")
    
    # Test with the load_document function and text_only=True
    content = list(load_document(str(file_path), extract_text_only=True))
    
    # Check that content was extracted
    assert content, "No content was extracted in text-only mode"
    
    # In text-only mode, we should have no HTML tags or Markdown syntax
    for chunk in content:
        assert "<h1>" not in chunk, "HTML tags found in text-only extraction"
        assert "<h2>" not in chunk, "HTML tags found in text-only extraction"
        assert "<p>" not in chunk, "HTML tags found in text-only extraction"
        assert "##" not in chunk, "Markdown syntax found in text-only extraction"
        assert "**" not in chunk, "Markdown syntax found in text-only extraction"
    
    # Check that the text content has reasonable length
    total_text = "".join(content)
    assert len(total_text) > 50, "Text content is suspiciously short"