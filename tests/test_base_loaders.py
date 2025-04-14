"""Tests for the base functionalities of loaders."""



from anydocs import AnyDocs
from anydocs._base import FileType

def test_file_type_enum():
    """Test that the FileType enum has the expected values."""
    assert FileType.DOCX.value == ".docx"
    assert FileType.PDF.value == ".pdf"
    assert FileType.CSV.value == ".csv"
    assert FileType.XML.value == ".xml"
    assert FileType.RTF.value == ".rtf"


def test_anydocs_registry():
    """Test that the AnyDocs registry contains all the expected loaders."""
    # Check that all standard extensions are in the registry
    for file_type in FileType:
        assert file_type.value in AnyDocs.get_registry()