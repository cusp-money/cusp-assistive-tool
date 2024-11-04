"""Base handler to analyze accounts data and add summary to google doc."""

from typing import Any


class FiDataAnalyzerBase:
    """Base class for FI data analyzers."""

    def write_summary_to_doc(
        self, xml_data: str, creds: Any, docs_service: Any, document_id: str
    ):
        """Writes summary to google doc."""
        raise NotImplementedError
