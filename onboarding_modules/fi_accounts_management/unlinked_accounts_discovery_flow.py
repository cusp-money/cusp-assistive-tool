"""Submodule for showing user's accounts not yet linked to AA."""

import num2words
import streamlit as st

from constants import saafe_constants
from onboarding_modules.login_signup import phone_number_verification_flow
from utils import saafe_utils


@st.dialog(title="Link account", width="small")
def verify_otp_dialog(
    phone_number: str,
    acc_key: str,
    masked_acc: str,
    discovered_account: str,
    signature: str,
    fip: str,
):
    """Handles account linking to saafe through OTP verification."""
    with st.status(
        label="Linking account to account aggregator...", expanded=True
    ) as link_status:
        st.write(
            f"OTP Sent to {phone_number}. "
            f"(Use {saafe_constants.ACCOUNT_LINKING_OTP}) for testing."
        )
        phone_number_verification_flow.reset_saafe_tokens()
        ref_number = saafe_utils.link_accounts(
            discovered_accounts=[discovered_account],
            signature=signature,
            saafe_access_token=st.session_state.saafe_access_token,
            fip_id=fip,
        )
        if not ref_number:
            st.error("Unable to link right now.")
            return
        otp = st.text_input(label="Enter OTP:", key=discovered_account)
        if st.button(f"Submit OTP to link {masked_acc}"):
            # Simulate OTP validation

            status = saafe_utils.account_link_verify_otp(
                ref_number=ref_number,
                otp=otp,
                fip_id=fip,
                saafe_access_token=st.session_state.saafe_access_token,
            )
            if status:
                st.session_state.link_status[acc_key]["linked"] = True
                st.rerun()
            else:
                st.error("Incorrect OTP. Please try again.")

    link_status.update(
        label="Account linked successfully",
        state="complete",
        expanded=True,
    )


def display_unlinked_fi_accounts(phone_number: str, all_fips: list):
    """Display all the unlinked accounts discovered against a mobile number."""
    with st.status(
        label="Discovering new accounts...", expanded=True
    ) as acc_discovery_status:
        # Discover accounts not yet linked to user's account.
        user_financial_accounts = []
        phone_number_verification_flow.reset_saafe_tokens()
        for bank in all_fips.get("BANK", []):
            data = saafe_utils.discover_accounts(
                phone_number=phone_number,
                fip_id=bank["id"],
                fip_types=saafe_constants.FI_TYPES,
                saafe_access_token=st.session_state.saafe_access_token,
            )

            if data and data["DiscoveredAccounts"]:
                user_financial_accounts.append(
                    {
                        "fip_name": bank["name"],
                        "fip_id": bank["id"],
                        "fip_logo": bank["logoUrl"],
                        "fip_data": bank,
                        "accounts": data["DiscoveredAccounts"],
                        "signature": data["signature"],
                    },
                )
        if not user_financial_accounts:
            st.header("No more new accounts discovered")
            st.markdown(
                (
                    "Let's move ahead and review the accounts which are "
                    "already linked."
                )
            )
            acc_discovery_status.update(
                label="New accounts discovery complete",
                state="complete",
                expanded=True,
            )
            return

        # Count total accounts discovered.
        num_acc = 0
        for fip_data in user_financial_accounts:
            num_acc += len(fip_data["accounts"])

        st.header(
            (
                f"Discovered {num2words.num2words(num_acc)} new "
                f"account{'s' if num_acc > 1 else ''}"
            )
        )
        st.markdown("Connect as many accounts as you wish.")
        st.markdown("More accounts equals more insights.")

        # Handle account linking
        if "link_status" not in st.session_state:
            st.session_state.link_status = {}

        for fip_data in user_financial_accounts:
            st.markdown(
                f"""
                <div style="display: flex; 
                            align-items: center; 
                            padding: 10px; 
                            border: 1px solid #ddd; 
                            border-radius: 8px; 
                            margin-bottom: 10px;">
                    <img src="{fip_data['fip_logo']}" 
                         alt="{fip_data['fip_name']}" 
                         style="width: 50px; 
                                height: 50px; 
                                margin-right: 10px;">
                    <div>
                        <h4 style="margin: 0; 
                            font-size: 1.2em;">{fip_data['fip_name']}</h4>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for idx, account in enumerate(fip_data["accounts"]):
                # Unique key for each account
                acc_key = (
                    f"{idx}_{fip_data['fip_name']}_"
                    f"{account['accRefNumber']}"
                )

                if acc_key not in st.session_state.link_status:
                    st.session_state.link_status[acc_key] = {"linked": False}

                # If account is linked, show green tick, else show button
                if st.session_state.link_status[acc_key]["linked"]:
                    st.markdown(
                        f"""
                        <div style="display: flex;
                                    align-items: center;
                                    padding: 10px; 
                                    border: 1px solid #28a745; 
                                    border-radius: 8px; 
                                    background-color: #d4edda; 
                                    margin-bottom: 10px;">
                            <span style="color: #155724; 
                                font-weight: bold;">
                                {account['maskedAccNumber']}
                            </span>
                            <span style="margin-left: auto;
                                         color: #28a745;">✅ Linked</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    # Show link button for accounts not yet linked
                    account_type = (
                        account["FIType"].replace("_", " ").capitalize()
                    )
                    if st.button(
                        "Link Account %s (%s)"
                        % (account["maskedAccNumber"], account_type),
                        key=acc_key,
                    ):
                        verify_otp_dialog(
                            phone_number=phone_number,
                            acc_key=acc_key,
                            masked_acc=account["maskedAccNumber"],
                            discovered_account=account,
                            signature=fip_data["signature"],
                            fip=fip_data["fip_id"],
                        )

        acc_discovery_status.update(
            label="New accounts discovery complete",
            state="complete",
            expanded=True,
        )
