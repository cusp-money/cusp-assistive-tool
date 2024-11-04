"""Analyzes life insurance data and adds summary to google doc."""

import xml.etree.ElementTree as ET
from typing import Any

from utils import google_docs_utils
from utils.fi_data_analysis.fi_data_analyzers import base_analyzer


class LifeInsuranceAnalyzer(base_analyzer.FiDataAnalyzerBase):
    """Analyzer for life insurance policy fi type."""

    def extract_life_insurance_policy_from_xml(
        self, xml_data: str
    ) -> list[list[str]]:
        """Extracts policy summary and transaction data from the XML string."""
        root = ET.fromstring(xml_data)
        ns = {"ns": "http://api.rebit.org.in/FISchema/life_insurance"}

        # Extract Summary data
        summary = root.find("ns:Summary", ns)
        summary_data = [
            ["Policy Type", summary.attrib["policyType"]],
            ["Status", summary.attrib["policyStatus"]],
            ["Sum Assured", summary.attrib["sumAssured"]],
            ["Tenure (Years)", summary.attrib["tenureYears"]],
            [
                "Premium Payment Duration",
                summary.attrib["premiumPaymentYears"],
            ],
            ["Premium Amount", summary.attrib["premiumAmount"]],
            ["Premium Frequency", summary.attrib["premiumFrequency"]],
            ["Policy Loan Status", summary.attrib["policyLoanStatus"]],
            ["Current Value", summary.attrib["currentValue"]],
            ["Assignment", summary.attrib["assignment"]],
            ["Surrender Value", summary.attrib["surrenderValue"]],
            ["Exclusions", summary.attrib["exclusions"]],
        ]

        return summary_data

    def write_summary_to_doc(
        self, xml_data: str, creds: Any, docs_service: Any, document_id: str
    ):
        """Writes life insurance policy summary to doc."""
        if isinstance(xml_data, str):
            xml_data = [xml_data]

        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id,
            docs_service=docs_service,
            heading="Life Insurance Policies",
        )

        for index, xml in enumerate(xml_data):
            # Extract data from XML
            summary_data = self.extract_life_insurance_policy_from_xml(
                xml_data=xml
            )

            # Write title and summary table to Google Doc
            google_docs_utils.write_title_to_google_doc(
                doc_id=document_id,
                docs_service=docs_service,
                title="Policy Details",
            )
            google_docs_utils.write_table_to_google_doc(
                table_data=summary_data,
                doc_id=document_id,
                creds=creds,
                docs_service=docs_service,
            )
