"""Submodule for fetching data from different accounts."""

import logging
import time
from typing import Optional

import streamlit as st

from constants import sahamatinet_constants
from utils.sahamati import sahamati_rahasya_utils, sahamatinet_utils


def fetch_data_though_sahamatinet_proxy(
    consent_id: str, account: dict, allowed_fetch_duration: tuple[str, str]
):
    """Fetches data for single account at a time."""
    # Get signed consent to generate session id
    signed_consent = sahamatinet_utils.fetch_consent(
        consent_id=consent_id,
        sahamatinet_member_token=st.session_state.sahamatinet_member_token,
    )
    if not signed_consent:
        return

    # Generate session id
    response = sahamatinet_utils.create_fi_request(
        consent_id=consent_id,
        signed_consent=signed_consent,
        sahamatinet_member_token=st.session_state.sahamatinet_member_token,
        start_date=allowed_fetch_duration["from"],
        end_date=allowed_fetch_duration["to"],
    )
    if not response:
        return
    session_id, our_nonce, our_private_key = response

    # Wait for data to be available and fetch once ready
    fetched_account_data = []

    trial = 0
    success = False

    while trial < sahamatinet_constants.MAX_TRIALS and not success:
        # SahamatiNet proxy returns simulated response for FI/fetch call.
        mock_params = {}
        if sahamatinet_constants.SIMULATE_FI_FETCH:
            mock_params = {
                "recipient-id": sahamatinet_constants.MOCK_AA_SIMULATOR,
                "x-scenario-id": f"{account['fiType']}_OK",
            }

        # Try to fetch data
        data = sahamatinet_utils.fi_fetch(
            accounts=[account["linkRefNumber"]],
            fip_id=account["fipHandle"],
            session_id=session_id,
            sahamatinet_member_token=st.session_state.sahamatinet_member_token,
            mock_params=mock_params,
        )

        trial += 1

        # If data not available then retry after configured time duration.
        if not data:
            logging.error(
                "Trial %s failed for %s. Retrying in %s seconds..."
                % (
                    trial,
                    account["linkRefNumber"],
                    sahamatinet_constants.DELAY_FOR_RETRY,
                )
            )
            time.sleep(sahamatinet_constants.DELAY_FOR_RETRY)

        logging.info(
            f"Success for {account['linkRefNumber']} on trial {trial}"
        )

        # Read encrypted fi data and decrypt it using our private key
        for fi_block in data["FI"]:
            for data_block in fi_block["data"]:
                encrypted_string = data_block["encryptedFI"]

                remote_key_material = fi_block["KeyMaterial"]
                remote_nonce = remote_key_material.pop("Nonce")

                if sahamatinet_constants.SIMULATE_FI_FETCH:
                    our_private_key = sahamatinet_constants.FIU_ECC_KEY_PAIR[
                        "privateKey"
                    ]
                    our_nonce = sahamatinet_constants.FIU_NONCE

                decrypted_string = sahamati_rahasya_utils.decrypt_fi_data(
                    encrypted_data=encrypted_string,
                    our_private_key=our_private_key,
                    remote_key_material=remote_key_material,
                    our_nonce=our_nonce,
                    remote_nonce=remote_nonce,
                )
                if decrypted_string:
                    fetched_account_data.append(decrypted_string)

        success = True

    return fetched_account_data


def fetch_data_for_all_linked_accounts(
    consent_id: str,
    accounts: list,
    allowed_fetch_duration: dict,
) -> Optional[list[dict]]:
    """Fetches data from accounts linked to consent and shows progress."""
    accounts_data = []

    with st.status(
        label="Fetching data...", expanded=True, state="running"
    ) as data_fetch_status:
        for account in accounts:
            fi_type_normalized = (
                account["fiType"].replace("_", " ").capitalize()
            )
            account_identifier = "%s (%s - %s)" % (
                account["fipName"],
                fi_type_normalized,
                account["maskedAccNumber"],
            )
            data_fetch_status.update(
                label=f"Fetching data for {account_identifier}...",
                state="running",
            )
            data = fetch_data_though_sahamatinet_proxy(
                consent_id=consent_id,
                account=account,
                allowed_fetch_duration=allowed_fetch_duration,
            )
            if data:
                display_str = (
                    f"Successfully fetched data for {account_identifier}"
                )
                data_fetch_status.update(label=display_str, state="running")
                st.success(display_str)
                accounts_data.append(
                    {
                        account_identifier: {
                            "fiType": account["fiType"],
                            "fiData": data,
                        }
                    }
                )
            else:
                display_str = f"Fail to fetch data for {account_identifier}"
                data_fetch_status.update(label=display_str, state="running")
                st.error(display_str)
            # break
            # TODO(remove this)
        data_fetch_status.update(
            label="Accounts data fetching complete",
            state="complete",
            expanded=False,
        )
    return accounts_data
