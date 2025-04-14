"""Test configuration and fixtures for the anydocs package."""
import shutil
import tempfile
from pathlib import Path
import requests

import pytest

# Define the test directory as a global variable
TEST_DIR = Path(tempfile.mkdtemp())

# Real-world test files from external sources
TEST_FILES = {
    "data.csv": "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/data.csv",
    "demo.docx": "https://calibre-ebook.com/downloads/demos/demo.docx",
    "search.html": "https://boto3.amazonaws.com/v1/documentation/api/latest/search.html",
    "example.jsonl": "https://raw.githubusercontent.com/anchen1011/chatgpt-finetune-ui/refs/heads/main/example.jsonl",
    "README.md": "https://raw.githubusercontent.com/bahamondeX/anytools/refs/heads/main/README.md",
    "libro-python.pdf": "https://uneweb.edu.ve/tuto-docs/libro-python.pdf",
    "nginx-for.pptx": "https://raw.githubusercontent.com/iancooper/Presentations/master/Nginx%20for.pptx",
    "codes.xlsx": "https://datos.canarias.es/api/estadisticas/structural-resources/v1.0/codelists/ISTAC/CL_MINISTERIO_TITULACIONES_FP/01.000/codes.xlsx",
    "sitemap.xml": "https://wordpress.com/sitemap.xml",
}


def download_file(url:str, destination:Path):
    """Download a file from a URL to a local destination."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        
        with open(destination.as_posix(), "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return False


@pytest.fixture(scope="session", autouse=True)
def setup_test_files():
    """Set up test files for the test suite."""
    # Create test files directory
    if not TEST_DIR.exists():
        TEST_DIR.mkdir(parents=True)
    
    # Download the real-world test files
    for filename, url in TEST_FILES.items():
        destination = TEST_DIR / filename
        if not download_file(url, destination):
            # If download fails, create a minimal file as fallback
            create_minimal_file(filename, destination)
            
    yield
    
    # Clean up after tests are done
    shutil.rmtree(TEST_DIR)


def create_minimal_file(filename:str, destination:Path):
    """Create a minimal test file if download fails."""
    extension = Path(filename).suffix.lower()
    
    content_map = {
        ".csv": "column1,column2\nvalue1,value2\n",
        ".docx": "Sample DOCX content - download failed",
        ".html": "<html><body><h1>Sample HTML</h1><p>Download failed</p></body></html>",
        ".jsonl": '{"text": "Sample JSONL content - download failed"}\n',
        ".md": "# Sample Markdown\n\nDownload failed\n",
        ".pdf": "Sample PDF content - download failed",
        ".pptx": "Sample PPTX content - download failed",
        ".xlsx": "Sample XLSX content - download failed",
        ".xml": "<?xml version=\"1.0\"?><root><item>Sample XML - download failed</item></root>",
    }
    
    # Get content based on extension or use a default
    content = content_map.get(extension, f"Sample content for {filename} - download failed")
    
    # Binary files need special handling
    binary_extensions = [".docx", ".pdf", ".pptx", ".xlsx"]
    
    if extension in binary_extensions:
        # For binary files, create an empty file
        with open(destination, "wb") as f:
            f.write(b"\x00\x01\x02\x03")  # Minimal binary content
    else:
        # For text files, write the content
        with open(destination, "w", encoding="utf-8") as f:
            f.write(content)


@pytest.fixture
def test_dir():
    """Return the test directory path."""
    return TEST_DIR


def get_test_file_path(filename:str):
    """Helper to get a test file path."""
    return TEST_DIR / filename