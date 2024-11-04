"""Submodule for phone number verification."""

import logging

import streamlit as st

from constants import saafe_constants
from utils import saafe_utils


def verify_user_entered_phone_number() -> str:
    """Submodule which authenticates user via OTP sent to phone number.

    Note that, for demo purpose we do not use our custom authentication instead
    we rely on Saafe AA's user authentication.
    """
    st.sidebar.header("Sign in / Sign up")

    # Initial state for OTP-related variables
    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False
    if "otp_validated" not in st.session_state:
        st.session_state.otp_validated = False

    st.sidebar.title("OTP Verification")

    # Step 1: Phone Number Input
    phone_number = st.sidebar.text_input("Enter your phone number:")

    # Step 2: OTP Button and Logic
    def get_otp():
        if phone_number:
            # Simulate OTP generation
            st.session_state.otp_sent = True
            st.sidebar.write("OTP sent to your phone!")
            st.sidebar.write(
                f"Use {saafe_constants.SAAFE_LOGIN_OTP} as OTP for testing."
            )  # Show OTP for testing

    # Step 3: OTP Input (Enabled after clicking 'Get OTP')
    if st.sidebar.button("Get OTP", on_click=get_otp):
        st.session_state.otp_sent = True

    otp = st.sidebar.text_input(
        "Enter OTP:", disabled=not st.session_state.otp_sent
    )

    # Step 4: OTP Validation
    def validate_otp():
        otp_unique_id = saafe_utils.request_otp_from_saafe(
            phone_number=phone_number
        )
        if not otp_unique_id or otp != saafe_constants.SAAFE_LOGIN_OTP:
            st.session_state.otp_validated = False
            st.error("Try again. OTP Verification failed.")
            return ""
        tokens = saafe_utils.verify_otp(
            phone_number=phone_number,
            otp_unique_id=otp_unique_id,
            otp=otp,
        )
        if not tokens:
            st.session_state.otp_validated = False
            st.error("Try again. OTP is incorrect.")
            return ""

        st.session_state.otp_validated = True
        st.success("OTP validated successfully!")
        (
            st.session_state.saafe_access_token,
            st.session_state.saafe_refresh_token,
        ) = tokens
        logging.info("Login successful.")

    # Step 5: Enable Submit OTP Button and Validate
    if st.sidebar.button(
        "Submit OTP",
        on_click=validate_otp,
        disabled=not st.session_state.otp_sent,
    ):
        if not st.session_state.otp_validated:
            st.sidebar.write("Please enter the correct OTP to proceed.")
            return ""

    # Footer at the bottom of the sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        (
            "<p style='text-align: center; font-size: 0.9em; color: grey;'>"
            "100% secure data sharing via RBI regulated Account Aggregator "
            "Saafe and supported by SahamatiNet</p>"
        ),
        unsafe_allow_html=True,
    )

    return phone_number


def reset_saafe_tokens():
    """Generates new set of auth tokens for saafe till refresh token expiry."""
    if st.session_state.saafe_refresh_token:
        tokens = saafe_utils.refresh_token(
            saafe_refresh_token=st.session_state.saafe_refresh_token
        )
        if tokens:
            (
                st.session_state.saafe_access_token,
                st.session_state.saafe_refresh_token,
            ) = tokens
        else:
            st.error("Session expired, please login again.")
            st.rerun()
