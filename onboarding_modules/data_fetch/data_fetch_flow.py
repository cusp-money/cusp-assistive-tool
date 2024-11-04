"""Submodule to fetch accounts data from consented FIPs."""

from typing import Optional

import streamlit as st

from onboarding_modules.data_fetch import (
    fetch_data_for_all_accounts,
    show_consent_used_for_data_fetch,
)
from onboarding_modules.login_signup import sahamatinet_login_flow


def fetch_accounts_data(
    consent_id: str, consent_handle: str, all_fips: list
) -> Optional[list[dict]]:
    """Shows consent being used and fetch accounts data."""
    data = []
    # Show the consent being used
    linked_acc_data = show_consent_used_for_data_fetch.show_active_consent(
        consent_handle=consent_handle,
        all_fips=all_fips,
    )
    if not linked_acc_data:
        return None
    accounts_linked_with_consent, allowed_fetch_duration = linked_acc_data

    # Fetch data for each account one by one
    if "sahamatinet_member_token" not in st.session_state:
        if not sahamatinet_login_flow.login_to_sahamatinet():
            st.error("Could not connect to SahamatiNet at the moment.")
            return None
    data = fetch_data_for_all_accounts.fetch_data_for_all_linked_accounts(
        consent_id=consent_id,
        accounts=accounts_linked_with_consent,
        allowed_fetch_duration=allowed_fetch_duration,
    )
    return data
