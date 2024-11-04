"""Analyzes equities data and adds summary to google doc."""

import xml.etree.ElementTree as ET
from typing import Any

from utils import google_docs_utils
from utils.fi_data_analysis.fi_data_analyzers import base_analyzer


class EquitiesAnalyzer(base_analyzer.FiDataAnalyzerBase):
    """Analyzer for equities fi type."""

    def extract_equities_summary_from_xml(
        self, xml_data: str
    ) -> list[list[str]]:
        """Extracts equities summary data from the given XML string."""
        root = ET.fromstring(xml_data)
        ns = {"ns": "http://api.rebit.org.in/FISchema/equities"}

        # Extract Summary data
        summary = root.find("ns:Summary", ns)
        current_value = summary.attrib["currentValue"]

        # Convert current value to a readable format
        current_value = "{:,.2f}".format(float(current_value))

        # Extract holdings
        holdings = summary.find("ns:Investment/ns:Holdings", ns)
        holdings_data = []

        for holding in holdings.findall("ns:Holding", ns):
            holding_data = {
                "Issuer Name": holding.attrib["issuerName"],
                "ISIN": holding.attrib["isin"],
                "Description": holding.attrib["isinDescription"],
                "Units": holding.attrib["units"],
                "Last Traded Price": holding.attrib["lastTradedPrice"],
            }
            holdings_data.append(holding_data)

        # Prepare the current value table
        value_table = [
            ["Current Value", current_value],
        ]

        # Prepare the holdings table
        holdings_table = [["Issuer Name", "Units", "Last Traded Price"]]

        for index, holding in enumerate(holdings_data, start=1):
            holdings_table.append(
                [
                    holding["Issuer Name"],
                    holding["Units"],
                    holding["Last Traded Price"],
                ]
            )

        return value_table, holdings_table

    def write_summary_to_doc(
        self, xml_data: str, creds: Any, docs_service: Any, document_id: str
    ):
        """Writes equities summary to doc."""
        if isinstance(xml_data, str):
            xml_data = [xml_data]

        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id, docs_service=docs_service, heading="Equities"
        )

        for index, xml in enumerate(xml_data):
            # Extract data from XML
            value_table, holdings_table = (
                self.extract_equities_summary_from_xml(xml)
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
