"""Submodule for discovery of any active consent granted by user."""

import streamlit as st

from onboarding_modules.login_signup import phone_number_verification_flow
from utils import saafe_utils


def set_active_consent(phone_number: str):
    """Sets the latest non-expired consent in session storage."""
    phone_number_verification_flow.reset_saafe_tokens()
    consents = saafe_utils.get_all_consents(
        saafe_access_token=st.session_state.saafe_access_token
    )
    if not consents:
        return
    latest_consent = saafe_utils.get_latest_valid_approved_consent(
        consents=consents
    )

    # Set active consent id and handle in streamlit session storage.
    if latest_consent:
        st.session_state.latest_consent_id = latest_consent["consentid"]
        st.session_state.latest_consent_handle = latest_consent[
            "consentHandle"
        ]
