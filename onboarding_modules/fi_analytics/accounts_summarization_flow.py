"""Submodule to handle account summary generation."""

from typing import Any

import streamlit as st

from constants import customer_profile_doc
from utils import api_utils, data_utils, google_docs_utils
from utils.fi_data_analysis import fi_data_analysis_utils
from utils.fi_data_analysis.fi_data_analyzers import base_analyzer


def get_new_doc_to_add_analysis(phone_number: str):
    """Creates a new google doc template for adding analysis."""
    # Create a new doc to store analysis.
    creds, docs_service, drive_service = (
        google_docs_utils.get_google_doc_creds()
    )

    doc_id = google_docs_utils.create_new_google_doc(
        docs_service=docs_service,
        title="%s - %s"
        % (
            customer_profile_doc.DOC_TITLE_PREFIX,
            api_utils.generate_transaction_id(),
        ),
    )

    # Give write access to advisor
    google_docs_utils.share_document(
        drive_service=drive_service,
        document_id=doc_id,
        email=customer_profile_doc.ADVISOR_EMAIL,
    )

    # Give viewer access to public
    google_docs_utils.share_document_publicly(
        drive_service=drive_service,
        document_id=doc_id,
        role="reader",
    )

    # Add a heading and description.
    google_docs_utils.write_heading_to_google_doc(
        doc_id=doc_id,
        docs_service=docs_service,
        heading=customer_profile_doc.AA_SUMMARY_HEADING,
        heading_level=1,
    )
    google_docs_utils.write_title_to_google_doc(
        doc_id=doc_id,
        docs_service=docs_service,
        title=customer_profile_doc.AA_SUMMARY_DESCRIPTION,
    )
    return doc_id


def add_summary_to_doc(
    account_id: str,
    account_data: list[dict],
    doc_id: str,
    status_handle: Any,
):
    """Adds analysis summary to google doc for data of given fi_type."""
    fi_type, xml_data = account_data["fiType"], account_data["fiData"]

    status_handle.update(
        label=f"Analyzing data for {account_id}...",
        state="running",
    )

    # Load suitable analyse for fi type and save results.
    analyse_and_save_fi_data: base_analyzer.FiDataAnalyzerBase = (
        fi_data_analysis_utils.get_fi_analysis_handler(fi_type=fi_type)
    )

    if analyse_and_save_fi_data is None:
        display_str = f"Failed to analyse {account_id} at this moment."
        status_handle.update(label=display_str, state="running")

    # Get creds and update google doc with analysis.
    creds, docs_service, _ = google_docs_utils.get_google_doc_creds()
    analyse_and_save_fi_data().write_summary_to_doc(
        xml_data=xml_data,
        creds=creds,
        docs_service=docs_service,
        document_id=doc_id,
    )

    display_str = f"Analyzed data for {account_id} successfully"
    status_handle.update(label=display_str, state="running")
    st.success(display_str)


def generate_summary_of_accounts(phone_number: str, accounts_data: list):
    """Generates summary of accounts and saves it in google doc."""
    with st.status(
        "Analyzing your accounts...", expanded=True, state="running"
    ) as analysis_status:
        if accounts_data:
            doc_id = get_new_doc_to_add_analysis(phone_number=phone_number)
            doc_link = f"https://docs.google.com/document/d/{doc_id}"
            st.markdown(
                f"Summary will be available in this [Google Doc]({doc_link})"
            )
        else:
            analysis_status.error(
                label="No accounts data found for analysis",
                expanded=False,
                state="error",
            )
            return

        # Add summary for different types of financial accounts such as
        # deposits, mutual funds and policies etc.
        for account_info in accounts_data:
            account_id, accounts_data = next(iter(account_info.items()))
            add_summary_to_doc(
                account_id=account_id,
                account_data=accounts_data,
                doc_id=doc_id,
                status_handle=analysis_status,
            )

        data_utils.save_locally(phone_number=phone_number, doc_id=doc_id)
        analysis_status.update(
            label="Account analysis complete", state="complete"
        )
