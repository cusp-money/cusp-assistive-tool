"""Submodule to show active consent being used for fetching data."""

from typing import Any, Optional

import streamlit as st

from onboarding_modules.consent_management import display_consent_summary_flow
from onboarding_modules.login_signup import phone_number_verification_flow
from utils import saafe_utils


def show_active_consent(
    consent_handle: str, all_fips: str
) -> Optional[tuple[Any]]:
    """Displays active consent being used for fetching data."""
    with st.status(
        "Showing active consent...", expanded=False, state="running"
    ) as active_consent:
        # Get consent summary for active consent.
        phone_number_verification_flow.reset_saafe_tokens()
        consent_summary = saafe_utils.get_consent_summary(
            consent_handle=consent_handle,
            saafe_access_token=st.session_state.saafe_access_token,
        )
        if not consent_summary:
            st.error("Unable to fetch consent summary at this moment.")
            active_consent.update(
                label="Could not fetch latest consent", state="error"
            )
            return None

        # Enrich metadata of accounts linked.
        accounts_linked_with_consent = (
            saafe_utils.get_linked_accounts_wth_enriched_data(
                saafe_access_token=st.session_state.saafe_access_token,
                all_fips=all_fips,
                consent_handle=consent_handle,
            )
        )
        if not accounts_linked_with_consent:
            st.error("Unable to fetch consent summary at this moment.")
            active_consent.update(
                label="Could not fetch latest consent", state="error"
            )
            return None

        # Display latest consent and linked financial accounts.
        display_consent_summary_flow.display_consent_summary(
            consent_summary=consent_summary,
            selected_accounts=accounts_linked_with_consent,
        )
        active_consent.update(
            label="Latest consent used for doing accounts analysis",
            state="complete",
        )

        allowed_fetch_duration = consent_summary["FIDataRange"]
        return accounts_linked_with_consent, allowed_fetch_duration
