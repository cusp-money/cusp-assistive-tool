"""Submodule to show the consent summary to the user."""

import datetime

import streamlit as st


def display_consent_summary(
    consent_summary: dict, selected_accounts: list = None
):
    """Shows the consent summary to the user along with account details."""
    # Convert dates from ISO format to readable format
    consent_start = datetime.datetime.fromisoformat(
        consent_summary["consentStart"].replace("Z", "+00:00")
    )
    consent_expiry = datetime.datetime.fromisoformat(
        consent_summary["consentExpiry"].replace("Z", "+00:00")
    )
    fi_data_from = datetime.datetime.fromisoformat(
        consent_summary["FIDataRange"]["from"].replace("Z", "+00:00")
    )
    fi_data_to = datetime.datetime.fromisoformat(
        consent_summary["FIDataRange"]["to"].replace("Z", "+00:00")
    )

    # Heading
    st.header("Consent Summary")

    # Display Data Consumer and FI Data Type Information
    st.write(
        "**What is our registered name?** %s"
        % consent_summary["DataConsumer"]["id"]
    )

    st.write(
        "**What can we do with your data?** %s"
        % consent_summary["consentMode"]
    )
    st.write(
        "**How many times can we fetch data?** %s"
        % consent_summary["fetchType"]
    )
    st.write(
        "**What type of accounts can we analyse?** %s"
        % ", ".join(consent_summary["fiTypes"])
    )

    # Display Purpose
    st.write("### Why do we need data?")
    st.write(consent_summary["Purpose"]["text"])

    # Display Linked Accounts
    if selected_accounts:
        st.write("### Which accounts can we analyse?")
        for account in selected_accounts:
            col1, col2 = st.columns([0.5, 4])
            with col1:
                st.image(account["logoUrl"], width=50)
            with col2:
                st.write(
                    "**%s** (%s)"
                    % (
                        account["fipName"],
                        account["fiType"].replace("_", " ").capitalize(),
                    )
                )
                st.write("Account Number: %s" % (account["maskedAccNumber"]))

    # Display FI Data Range and Consent Duration
    st.write("### Which transactions can we fetch?")
    st.write(
        "Starting from %s till %s"
        % (fi_data_from.strftime("%d %b %Y"), fi_data_to.strftime("%d %b %Y"))
    )

    st.write("### What is the validity of this consent?")
    st.write(
        "Starting from %s only till %s"
        % (
            consent_start.strftime("%d %b %Y"),
            consent_expiry.strftime("%d %b %Y"),
        )
    )

    st.write("### What information will be shared by providers?")
    st.write(", ".join(consent_summary["consentTypes"]))
