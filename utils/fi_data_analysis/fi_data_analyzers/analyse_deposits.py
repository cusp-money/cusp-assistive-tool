"""Analyzes deposits data and adds summary to google doc."""

import xml.etree.ElementTree as ET
from typing import Any

import pandas as pd

from utils import google_docs_utils
from utils.fi_data_analysis.fi_data_analyzers import base_analyzer
from utils.text_processing import predict_transactions_tags


class DepositsAnalyzer(base_analyzer.FiDataAnalyzerBase):
    """Analyzer for deposits fi type."""

    def parse_multiple_xmls_to_df(self, xml_list: list[str]) -> pd.DataFrame:
        """Extracts transaction data and concatenates them into a single df."""
        all_transactions = []

        for xml_data in xml_list:
            # Parse each XML data
            root = ET.fromstring(xml_data)

            # Define the namespace
            ns = {"ns": "http://api.rebit.org.in/FISchema/deposit"}

            # Extract transactions and add to the list
            transactions = [
                {
                    "remark": transaction.get("narration"),
                    "date": transaction.get("valueDate"),
                    "amount": transaction.get("amount"),
                    "transaction_type": transaction.get("type"),
                }
                for transaction in root.findall(
                    ".//ns:Transaction", namespaces=ns
                )
            ]

            all_transactions.extend(transactions)

        # Convert the list of all transactions to a DataFrame
        df = pd.DataFrame(
            all_transactions,
            columns=[
                "remark",
                "date",
                "amount",
                "transaction_type",
            ],
        )

        return df

    def extract_savings_account_balances_from_xml(
        self, xml_list: list[str]
    ) -> list[list[str]]:
        """Extracts current balances from a list of savings account XMLs."""
        total_balance = 0.0
        balance_data = []

        for xml_data in xml_list:
            root = ET.fromstring(xml_data)
            ns = {"ns": "http://api.rebit.org.in/FISchema/deposit"}

            # Extract Summary data
            summary = root.find("ns:Summary", ns)
            current_balance = float(summary.attrib["currentBalance"])
            currency = summary.attrib["currency"]

            # Append the balance data to the list
            balance_data.append(
                {
                    "Current Balance": "{:,.2f} {}".format(
                        current_balance, currency
                    ),
                }
            )

            # Add to total balance
            total_balance += current_balance

        # Prepare the table header
        table_header = ["No.", "Current Balance"]

        # Prepare the balance table
        balance_table = [table_header]

        for index, data in enumerate(balance_data, start=1):
            balance_table.append(
                [
                    f"Account {index}",
                    data["Current Balance"],
                ]
            )

        # Add total balance row
        balance_table.append(
            ["Total", "{:,.2f} {}".format(total_balance, currency)]
        )

        return balance_table

    def calculate_avg_monthly_amounts(
        self,
        transactions_df: pd.DataFrame,
    ) -> list[list[str]]:
        """Calculates average monthly incoming and outgoing amounts."""
        # Ensure amount is numeric and convert if necessary
        transactions_df["amount_num"] = pd.to_numeric(
            transactions_df["amount"], errors="coerce"
        )

        # Convert the 'date' column to datetime format
        transactions_df["datetime"] = pd.to_datetime(transactions_df["date"])

        # Separate incoming and outgoing amounts
        transactions_df["month"] = transactions_df["datetime"].dt.to_period(
            "M"
        )

        # Calculate total incoming and outgoing amounts per month
        total_amounts = (
            transactions_df.groupby(["month", "transaction_type"])[
                "amount_num"
            ]
            .sum()
            .unstack(fill_value=0)
        )

        # Calculate averages per month
        avg_incoming = total_amounts.get("CREDIT", 0).mean()
        avg_outgoing = total_amounts.get("DEBIT", 0).mean()

        # Round to two decimal places and convert to string
        avg_incoming_rounded = str(round(avg_incoming, 2))
        avg_outgoing_rounded = str(round(avg_outgoing, 2))

        # Convert total_amounts DataFrame to list of lists and convert month to
        # string
        total_amounts_list = total_amounts.reset_index()
        total_amounts_list["month"] = total_amounts_list["month"].astype(
            str
        )  # Convert Period to string
        total_amounts_list["CREDIT"] = total_amounts_list["CREDIT"].astype(
            str
        )  # Convert Period to string
        total_amounts_list["DEBIT"] = total_amounts_list["DEBIT"].astype(
            str
        )  # Convert Period to string

        total_amounts_list = [
            ["Month", "Total incoming amount", "Total outgoing amount"]
        ] + total_amounts_list.values.tolist()

        # Select only the columns we want and convert to a list of lists
        averages_list = [
            [
                "",
                "Avg. monthly incoming amount",
                "Avg. monthly outgoing amount",
            ]
        ]
        averages_list.append(["", avg_incoming_rounded, avg_outgoing_rounded])

        # Append the averages at the end
        total_amounts_list.extend(averages_list)

        return total_amounts_list

    def get_percentage_summary_by_tags(
        self, predictions_df: pd.DataFrame, use_subcategory: bool = False
    ) -> list[list[str]]:
        """Gets the percentage summary by tags."""
        # Calculate percentage summary
        aggregate_over = (
            "predicted_subcategory"
            if use_subcategory
            else "predicted_category"
        )
        tmp_out = (
            predictions_df[aggregate_over].value_counts(normalize=True) * 100
        )

        # Calculate average amount by tag
        average_amounts = predictions_df.groupby(aggregate_over)[
            "amount_num"
        ].mean()

        # Create a DataFrame for the summary
        summary_df = pd.DataFrame(
            {
                "Category": tmp_out.index,
                "Percentage": tmp_out.values,
                "Average Amount": average_amounts[tmp_out.index].values,
            }
        )

        # Round and convert to string
        summary_df["Percentage"] = (
            summary_df["Percentage"].round(2).astype(str)
        )
        summary_df["Average Amount"] = (
            summary_df["Average Amount"].round(2).astype(str)
        )

        # Prepare summary with headers included
        category_wise_summary = [
            summary_df.columns.tolist()
        ] + summary_df.values.tolist()
        return category_wise_summary

    def write_summary_to_doc(
        self, xml_data: str, creds: Any, docs_service: Any, document_id: str
    ):
        """Writes deposits summary to doc."""
        if isinstance(xml_data, str):
            xml_data = [xml_data]

        # Write title and summary table to Google Doc
        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id,
            docs_service=docs_service,
            heading="Bank accounts",
        )
        balance_table = self.extract_savings_account_balances_from_xml(
            xml_list=xml_data
        )
        google_docs_utils.write_table_to_google_doc(
            table_data=balance_table,
            doc_id=document_id,
            creds=creds,
            docs_service=docs_service,
        )

        # Write category wise summary to Google doc
        transactions_df = self.parse_multiple_xmls_to_df(xml_list=xml_data)

        # Write monthly average amount
        monthly_avg = self.calculate_avg_monthly_amounts(
            transactions_df=transactions_df
        )
        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id,
            docs_service=docs_service,
            heading="Cash Flow Analysis",
            heading_level="3",
        )
        google_docs_utils.write_table_to_google_doc(
            table_data=monthly_avg,
            doc_id=document_id,
            creds=creds,
            docs_service=docs_service,
        )

        # Write category wise summary for credit and debit transactions.
        debit_trxn_tags, credit_trxn_tags = (
            predict_transactions_tags.get_debit_and_credit_transactions_tags(
                transactions_df=transactions_df
            )
        )
        debit_summary = self.get_percentage_summary_by_tags(
            predictions_df=debit_trxn_tags
        )
        credit_summary = self.get_percentage_summary_by_tags(
            predictions_df=credit_trxn_tags, use_subcategory=True
        )

        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id,
            docs_service=docs_service,
            heading="Debit transactions summary",
            heading_level="4",
        )
        google_docs_utils.write_table_to_google_doc(
            table_data=debit_summary,
            doc_id=document_id,
            creds=creds,
            docs_service=docs_service,
        )

        google_docs_utils.write_heading_to_google_doc(
            doc_id=document_id,
            docs_service=docs_service,
            heading="Credit transactions summary",
            heading_level="4",
        )
        google_docs_utils.write_table_to_google_doc(
            table_data=credit_summary,
            doc_id=document_id,
            creds=creds,
            docs_service=docs_service,
        )
