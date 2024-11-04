"""Submodule to handle SahamatiNet FIU authentication."""

import streamlit as st

from constants import sahamatinet_constants
from utils.sahamati import sahamatinet_utils


def login_to_sahamatinet() -> bool:
    """Handles login to sahamatinet."""
    if "sahamatinet_member_token" not in st.session_state:
        # Generate user token
        user_token = sahamatinet_utils.get_sahamatinet_user_token(
            sahamatinet_user_name=sahamatinet_constants.USER_NAME,
            sahamatinet_password=sahamatinet_constants.PASSWORD,
        )
        if not user_token:
            return False

        # Read member secret
        member_secret = sahamatinet_utils.get_sahamatinet_member_secret(
            sahamatinet_member_id=sahamatinet_constants.MEMBER_ID,
            sahamatinet_user_token=user_token,
        )
        if not member_secret:
            return False

        # Generate member token
        member_token = sahamatinet_utils.get_sahamatinet_member_token(
            sahamatinet_member_id=sahamatinet_constants.MEMBER_ID,
            sahamatinet_member_secret=member_secret,
        )
        if not member_token:
            return False

        # Set member token in session memory for later use.
        st.session_state.sahamatinet_member_token = member_token
    return True
