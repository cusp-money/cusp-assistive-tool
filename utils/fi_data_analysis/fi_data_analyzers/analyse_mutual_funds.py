"""Analyzes mutual funds data and adds summary to google doc."""

import xml.etree.ElementTree as ET
from typing import Any

from utils import google_docs_utils
from utils.fi_data_analysis.fi_data_analyzers import base_analyzer


class MutualFundsAnalyzer(base_analyzer.FiDataAnalyzerBase):
    """Analyzer for mutual funds fi type."""

    def extract_mutual_funds_summary_from_xml(
        self, xml_data: str
    ) -> list[list[str]]:
        """Extracts mutual funds summary data from the given XML string."""
        root = ET.fromstring(xml_data)
        ns = {"ns": "http://api.rebit.org.in/FISchema/mutual_funds"}

        # Extract Summary data
        summary = root.find("ns:Summary", ns)
        cost_value = summary.attrib["costValue"]
        current_value = summary.attrib["currentValue"]

        # Convert current value from scientific notation to a more readable
        # format
        current_value = "{:,.2f}".format(float(current_value))

        # Extract holdings
        holdings = summary.find("ns:Investment/ns:Holdings", ns)
        holdings_data = []

        for holding in holdings.findall("ns:Holding", ns):
            holding_data = {
                "AMC": holding.attrib["amc"],
                "Scheme Code": holding.attrib["schemeCode"],
                "Option": holding.attrib["schemeOption"],
                "Category": holding.attrib["schemeCategory"],
                "NAV": holding.attrib["nav"],
                "Units": holding.attrib["closingUnits"],
                "FATCA Status": holding.attrib["FatcaStatus"],
                "Folio No": holding.attrib["folioNo"],
            }
            holdings_data.append(holding_data)

        # Prepare the cost and current value table
        value_table = [
            ["Cost Value", "{:,.2f}".format(float(cost_value))],
            ["Current Value", current_value],
        ]

        # Prepare the holdings table
        holdings_table = [
            ["AMC", "Scheme Code", "Option", "Category", "NAV", "Units"]
        ]

        for holding in holdings_data:
            holdings_table.append(
                [
                    holding["AMC"],
                    holding["Scheme Code"],
                    holding["Option"],
                    holding["Category"],
                    holding["NAV"],
                    holding["Units"],
                ]
            )

        return value_table, holdings_table

    def write_summary_to_doc(
        self, xml_data: str, creds: Any, docs_service: Any, document_id: str
    ):
        """Writes mutual funds summary to doc."""
        if isinstance(xml_data, str):
            xml_data = [xml_data]

        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id,
            docs_service=docs_service,
            heading="Mutual Funds",
        )

        for index, xml in enumerate(xml_data):
            # Extract data from XML
            value_table, holdings_table = (
                self.extract_mutual_funds_summary_from_xml(xml_data=xml)
            )

            # Write title and summary table to Google Doc
            google_docs_utils.write_title_to_google_doc(
                doc_id=document_id,
                docs_service=docs_service,
                title=f"Broker {index+1}",
            )
            google_docs_utils.write_table_to_google_doc(
                table_data=value_table,
                doc_id=document_id,
                creds=creds,
                docs_service=docs_service,
            )
            google_docs_utils.write_table_to_google_doc(
                table_data=holdings_table,
                doc_id=document_id,
                creds=creds,
                docs_service=docs_service,
            )
