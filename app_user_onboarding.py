"""Streamlit app for user onboarding and account aggregation."""

import logging
from typing import Optional

import streamlit as st

from onboarding_modules.consent_management import (
    active_consent_discovery_flow,
    request_new_consent_flow,
)
from onboarding_modules.data_fetch import data_fetch_flow
from onboarding_modules.fi_analytics import accounts_summarization_flow
from onboarding_modules.informational_screens import (
    about_cuspmoney,
    advice_pending,
    advice_qa_over_call,
    initial_call,
)
from onboarding_modules.login_signup import phone_number_verification_flow
from utils import onboarding_utils, saafe_utils

UserJourneyStage = onboarding_utils.UserJourneyStage


def fetch_data_from_consented_fips(phone_number: str) -> Optional[list[dict]]:
    """Fetches data from consented financial information providers."""
    # Get list of all the FIPs integrated with Saafe AA.
    accounts_data = []
    phone_number_verification_flow.reset_saafe_tokens()
    all_fips = saafe_utils.get_all_fips(
        saafe_access_token=st.session_state.saafe_access_token
    )
    if not all_fips:
        st.error(
            "Unable to find any financial information providers at this moment"
        )
        return None

    # Check if consent is already granted.
    if "latest_consent_id" not in st.session_state:
        active_consent_discovery_flow.set_active_consent(
            phone_number=phone_number
        )

    # If no active consent is found then request a new one.
    if "latest_consent_id" not in st.session_state:
        request_new_consent_flow.get_new_consent_from_user(
            phone_number=phone_number, all_fips=all_fips
        )

    # Fetch data if consent is already granted.
    if "latest_consent_id" in st.session_state:
        accounts_data = data_fetch_flow.fetch_accounts_data(
            consent_id=st.session_state.latest_consent_id,
            consent_handle=st.session_state.latest_consent_handle,
            all_fips=all_fips,
        )

    return accounts_data


def main():
    """Root of account aggregation portal."""
    # Show basic information about Cusp Money.
    st.set_page_config(page_title="Cusp Money Onboarding", page_icon=":bank:")
    st.title("Cusp Money - A step towards financial inclusion.")
    if "saafe_access_token" not in st.session_state:
        about_cuspmoney.show_cusp_info()
        # CTA for login.
        st.markdown(
            (
                "<h5 style='color: grey;'>Sign in with your phone number to "
                "get started.</h1>"
            ),
            unsafe_allow_html=True,
        )

    # Handle Login or signup.
    verified_phone_number = (
        phone_number_verification_flow.verify_user_entered_phone_number()
    )
    if "saafe_access_token" not in st.session_state:
        return  # Not yet logged in

    # Check user's state in onboarding journey.
    user_journey_state: UserJourneyStage = (
        onboarding_utils.detect_user_journey_state(
            phone_number=verified_phone_number
        )
    )
    logging.info(f"Current state of user is : {user_journey_state.name}")

    # Handle different user journey stages.
    match user_journey_state:
        # User is yet to share account aggregator data.
        case UserJourneyStage.AA_DATA_PENDING:
            accounts_data = fetch_data_from_consented_fips(
                phone_number=verified_phone_number
            )

            # Analyse account aggregator data.
            if accounts_data:
                accounts_summarization_flow.generate_summary_of_accounts(
                    phone_number=verified_phone_number,
                    accounts_data=accounts_data,
                )
                # CTA for calling to cusp for 1:1 conversation.
                initial_call.suggest_user_to_call_cusp_ai_agent()

        # CTA for calling to cusp for 1:1 conversation.
        case UserJourneyStage.CUSTOMER_PROFILE_PENDING:
            initial_call.suggest_user_to_call_cusp_ai_agent()

        # Suggest user that advisor has not completed advise generation
        case UserJourneyStage.ADVICE_GENERATION_PENDING:
            advice_pending.suggest_user_about_advice_pending()

        # Suggest user that advise is ready and call voice assistant to
        # understand it.
        case UserJourneyStage.ADVICE_EXISTS:
            advice_qa_over_call.call_cusp_ai_for_qa_over_advise()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()
