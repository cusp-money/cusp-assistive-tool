"""Analyzes recurrent deposits data and adds summary to google doc."""

import datetime
import xml.etree.ElementTree as ET
from typing import Any

from utils import google_docs_utils
from utils.fi_data_analysis.fi_data_analyzers import base_analyzer


class RecurrentDepositsAnalyzer(base_analyzer.FiDataAnalyzerBase):
    """Analyzer for recurrent deposits fi type."""

    def extract_recurring_deposit_summary_from_xml(
        self, xml_data: str
    ) -> list[list[str]]:
        """Extracts summary data from the XML string for recurring deposits."""
        root = ET.fromstring(xml_data)
        ns = {"ns": "http://api.rebit.org.in/FISchema/recurring_deposit"}

        # Extract Summary data
        summary = root.find("ns:Summary", ns)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        summary_data = [
            ["Description", summary.attrib["description"]],
            ["Opening Date", summary.attrib["openingDate"]],
            ["Maturity Amount", summary.attrib["maturityAmount"]],
            ["Maturity Date", summary.attrib["maturityDate"]],
            ["Interest Payout", summary.attrib["interestPayout"]],
            ["Interest Rate (%)", summary.attrib["interestRate"]],
            ["Principal Amount", summary.attrib["principalAmount"]],
            ["Recurring Amount", summary.attrib["recurringAmount"]],
            ["Recurring Deposit Day", summary.attrib["recurringDepositDay"]],
            ["Interest Computation", summary.attrib["interestComputation"]],
            ["Compounding Frequency", summary.attrib["compoundingFrequency"]],
            ["Interest on Maturity", summary.attrib["interestOnMaturity"]],
            [
                f"Current Value (As on {today_date})",
                f"{summary.attrib['currentValue']}",
            ],
        ]

        return summary_data

    def write_summary_to_doc(
        self, xml_data: str, creds: Any, docs_service: Any, document_id: str
    ):
        """Writes recurrent deposits summary to doc."""
        if isinstance(xml_data, str):
            xml_data = [xml_data]

        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id,
            docs_service=docs_service,
            heading="Recurrent Deposits",
        )
        for index, xml in enumerate(xml_data):
            # Extract data from XML
            summary_data = self.extract_recurring_deposit_summary_from_xml(xml)

            # Write title and summary table to Google Doc
            google_docs_utils.write_title_to_google_doc(
                doc_id=document_id,
                docs_service=docs_service,
                title=f"RD {index+1} Details",
            )
            google_docs_utils.write_table_to_google_doc(
                table_data=summary_data,
                doc_id=document_id,
                creds=creds,
                docs_service=docs_service,
            )
