"""Tests for PowerPoint (PPTX) loader using real-world files."""

import pytest
from pathlib import Path

from anydocs import PptxLoader, load_document
from tests.conftest import get_test_file_path


def test_pptx_loader_with_real_file():
    """Test the PPTX loader with a real PowerPoint file."""
    file_path = get_test_file_path("nginx-for.pptx")
    
    # Test direct loader usage
    loader = PptxLoader(ref=str(file_path))
    content = list(loader.extract())
    
    # Check that content was extracted
    assert content, "No content was extracted from the PPTX file"
    
    # Check for slide markers or content
    slide_content_found = False
    for chunk in content:
        # Look for paragraph content or slide headers 
        if "<h2>Slide " in chunk or "<p>" in chunk:
            slide_content_found = True
            break
    
    assert slide_content_found, "No slide content found in extracted content"
    
    # Check for Nginx references (it's an Nginx presentation)
    nginx_references_found = False
    total_content = "".join(content)
    if "Nginx" in total_content or "nginx" in total_content or "NGINX" in total_content:
        nginx_references_found = True
    
    assert nginx_references_found, "No Nginx references found in the Nginx presentation"


def test_pptx_load_document():
    """Test loading a PPTX file using the top-level load_document function."""
    file_path = get_test_file_path("nginx-for.pptx")
    
    # Test with the load_document function
    content = list(load_document(str(file_path)))
    
    # Check that content was extracted
    assert content, "No content was extracted using load_document"
    
    # The presentation should have multiple slides
    slides_found = 0
    for chunk in content:
        if "<h2>Slide " in chunk:
            slides_found += 1
    
    assert slides_found > 0, f"Expected multiple slides, but found {slides_found}"
    
    # Check for image extraction (if any)
    images_found = False
    for chunk in content:
        if "<img" in chunk and "base64" in chunk:
            images_found = True
            break
    
    # Note: Not all presentations have images, so this is merely informative
    if not images_found:
        print("Info: No images found in the PPTX file")


def test_pptx_text_extraction():
    """Test extracting plain text from a PPTX file."""
    file_path = get_test_file_path("nginx-for.pptx")
    
    # Test with the load_document function and text_only=True
    content = list(load_document(str(file_path), extract_text_only=True))
    
    # Check that content was extracted
    assert content, "No content was extracted in text-only mode"
    
    # In text-only mode, we should have no HTML tags
    for chunk in content:
        assert "<p>" not in chunk, "HTML paragraph tags found in text-only extraction"
        assert "<h2>" not in chunk, "HTML header tags found in text-only extraction"
        assert "<img" not in chunk, "HTML image tags found in text-only extraction"
    
    # Check that the text content has reasonable length
    total_text = "".join(content)
    assert len(total_text) > 50, "Text content is suspiciously short for a presentation"
    
    # Check for presentation-related terms in the content
    assert "Nginx" in total_text or "nginx" in total_text or "NGINX" in total_text, \
        "Expected Nginx references not found in text content"