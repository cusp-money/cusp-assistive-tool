"""Submodule for requesting a new consent approval from user."""

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from constants import sahamatinet_constants
from onboarding_modules.consent_management import display_consent_summary_flow
from onboarding_modules.fi_accounts_management import (
    linked_accounts_selection_flow,
    unlinked_accounts_discovery_flow,
)
from onboarding_modules.login_signup import (
    phone_number_verification_flow,
    sahamatinet_login_flow,
)
from utils import saafe_utils
from utils.sahamati import sahamatinet_utils


@st.dialog(title="Authorize Cusp Money", width="large")
def consent_approval_flow(
    phone_number: str, existing_accounts: list, selected_accounts: set
):
    """Presents the consent details to the user and handles approval."""
    with st.status(
        label="Preparing consent...", expanded=True, state="running"
    ) as consent_status:
        # Get list of selected accounts.
        selected_accounts_details_for_display = []
        selected_accounts_for_consent_approval = []
        selected_accounts_fi_types = set()
        for account_ref in selected_accounts:
            account = next(
                (
                    acc
                    for acc in existing_accounts
                    if acc["linkRefNumber"] == account_ref
                ),
                None,
            )
            if account:
                selected_accounts_details_for_display.append(account)
                selected_accounts_for_consent_approval.append(
                    {
                        "linkRefNumber": account["linkRefNumber"],
                        "fipHandle": account["fipHandle"],
                    }
                )
                selected_accounts_fi_types.add(account["fiType"])

        # Generate consent id
        consent_handle = sahamatinet_utils.create_consent(
            phone_number=phone_number,
            fi_types=list(selected_accounts_fi_types),
            sahamatinet_member_token=st.session_state.sahamatinet_member_token,
            sahamatinet_member_id=sahamatinet_constants.MEMBER_ID,
        )
        if not consent_handle:
            st.error("Consent creation failed, try again.")
            return

        # Get consent summary from AA
        phone_number_verification_flow.reset_saafe_tokens()
        consent_status.update(
            label="Fetching consent details from Saafe AA...", expanded=True
        )
        consent_summary = saafe_utils.get_consent_summary(
            consent_handle=consent_handle,
            saafe_access_token=st.session_state.saafe_access_token,
        )

        # Display consent summary along with selected accounts
        consent_status.update(
            label="Consent approval is pending", expanded=True, state="running"
        )

        display_consent_summary_flow.display_consent_summary(
            consent_summary=consent_summary,
            selected_accounts=selected_accounts_details_for_display,
        )

        # Handle consent approval
        with stylable_container(
            "green",
            css_styles="""
            button {
                background-color: #c9ffdb;
                color: black;
            }""",
        ):
            if st.button("Approve Consent", use_container_width=True):
                # Approve the consent
                saafe_utils.set_consent_state(
                    consent_handle=consent_handle,
                    selected_accounts=selected_accounts_for_consent_approval,
                    saafe_access_token=st.session_state.saafe_access_token,
                    consent_approval_status="READY",
                )
                st.success("Consent approved! You may close this now.")
                st.session_state.selected_accounts = set()
                consent_status.update(
                    label="Consent flow completed", state="complete"
                )
                st.rerun()


def get_new_consent_from_user(phone_number: str, all_fips: list):
    """Gets a new approval from user for sharing accounts data."""
    # Show option to link accounts with AA.
    unlinked_accounts_discovery_flow.display_unlinked_fi_accounts(
        phone_number=phone_number, all_fips=all_fips
    )

    # Show option to select linked accounts for consent approval.
    phone_number_verification_flow.reset_saafe_tokens()
    existing_accounts = saafe_utils.get_linked_accounts_wth_enriched_data(
        saafe_access_token=st.session_state.saafe_access_token,
        all_fips=all_fips,
    )
    linked_accounts_selection_flow.show_linked_accounts_with_checkboxes(
        linked_accounts=existing_accounts
    )

    # Allow user to review consent and approves it.
    if st.button("Share selected accounts"):
        if st.session_state.selected_accounts:
            if sahamatinet_login_flow.login_to_sahamatinet():
                consent_approval_flow(
                    phone_number=phone_number,
                    existing_accounts=existing_accounts,
                    selected_accounts=st.session_state.selected_accounts,
                )
            else:
                st.warning(
                    "Could not connect to SahamatiNet right now, try later."
                )
        else:
            st.warning("Please select at least one account to give consent.")
