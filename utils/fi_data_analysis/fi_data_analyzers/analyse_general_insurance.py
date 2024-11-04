"""Analyzes general insurance data and adds summary to google doc."""

import xml.etree.ElementTree as ET
from typing import Any

from utils import google_docs_utils
from utils.fi_data_analysis.fi_data_analyzers import base_analyzer


class GeneralInsuranceAnalyzer(base_analyzer.FiDataAnalyzerBase):
    """Analyzer for general insurance fi type."""

    def extract_general_insurance_summary_from_xml(
        self, xml_data: str
    ) -> list[list[str]]:
        """Extracts policy summary data from the given XML string."""
        root = ET.fromstring(xml_data)
        ns = {"ns": "http://api.rebit.org.in/FISchema/general_insurance"}

        # Extract Summary data
        summary = root.find("ns:Summary", ns)
        summary_data = [
            ["Policy Name", summary.attrib["policyName"]],
            ["Policy Description", summary.attrib["policyDescription"]],
            ["Sum Assured", summary.attrib["sumAssured"]],
            ["Tenure (Months)", summary.attrib["tenureMonths"]],
            ["Premium Amount", summary.attrib["premiumAmount"]],
            ["Policy Start Date", summary.attrib["policyStartDate"]],
            ["Policy Expiry Date", summary.attrib["policyExpiryDate"]],
            ["Policy Type", summary.attrib["policyType"]],
            ["Insurance Type", summary.attrib["insuranceType"]],
            ["Premium Frequency", summary.attrib["premiumFrequency"]],
            ["Premium Payment Years", summary.attrib["premiumPaymentYears"]],
            ["Next Premium Due Date", summary.attrib["nextPremiumDueDate"]],
            ["Policy Status", summary.attrib["policyStatus"]],
        ]

        return summary_data

    def write_summary_to_doc(
        self, xml_data: str, creds: Any, docs_service: Any, document_id: str
    ):
        """Writes general insurance summary to doc."""
        if isinstance(xml_data, str):
            xml_data = [xml_data]

        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id,
            docs_service=docs_service,
            heading="General Insurance Policies",
        )

        for index, xml in enumerate(xml_data):
            # Extract data from XML
            summary_data = self.extract_general_insurance_summary_from_xml(
                xml_data=xml
            )

            # Write title and summary table to Google Doc
            google_docs_utils.write_title_to_google_doc(
                doc_id=document_id,
                docs_service=docs_service,
                title=f"Policy {index+1} Details",
            )
            google_docs_utils.write_table_to_google_doc(
                table_data=summary_data,
                doc_id=document_id,
                creds=creds,
                docs_service=docs_service,
            )
