"""Helper library to consume Saafe account aggregator APIs."""

import datetime
import logging
from typing import Optional

from constants import saafe_constants
from utils import api_utils

# Authentication APIs


def request_otp_from_saafe(phone_number: str) -> Optional[str]:
    """Registers a new phone number with Saafe if not exists and sends OTP."""
    payload = {"phoneNumber": phone_number, "isTermsAndConditionAgreed": True}
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="POST",
        endpoint="/public/user/combined/init-otp",
        payload=payload,
    )

    if response and "otpUniqueID" in response:
        return response["otpUniqueID"]
    logging.error("OTP could not be sent.")
    return None


def verify_otp(
    phone_number: str, otp: str, otp_unique_id: str
) -> Optional[tuple[str]]:
    """Verifies otp sent from saafe aa to a registered phone number."""
    payload = {
        "phoneNumber": phone_number,
        "code": otp,
        "otpUniqueID": otp_unique_id,
    }
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="POST",
        endpoint="/public/user/combined/verify-otp",
        payload=payload,
    )

    if response:
        return response.get("access_token"), response.get("refresh_token")
    logging.error("OTP Verify failed.")
    return None, None


def refresh_token(saafe_refresh_token: str) -> Optional[tuple[str]]:
    """Verifies otp sent from saafe aa to a registered phone number."""
    payload = {
        "refreshToken": saafe_refresh_token,
    }
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="POST",
        endpoint="/public/user/refreshtoken",
        payload=payload,
    )

    if response:
        return response.get("access_token"), response.get("refresh_token")
    logging.error("Failed to refresh saafe tokens.")
    return None, None


def get_linked_accounts(
    saafe_access_token: str, consent_handle: Optional[str] = None
) -> Optional[list]:
    """Retrieves user's accounts already linked to saafe."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {saafe_access_token}",
    }

    endpoint = "/User/linkedaccount"
    if consent_handle is not None:
        endpoint += f"?consentHandle={consent_handle}"

    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="GET",
        endpoint=endpoint,
        headers=headers,
    )

    if response:
        return response
    logging.error("Failed to get list of accounts linked with saafe.")
    return None


# Accounts APIs


def get_all_fips(saafe_access_token: str) -> Optional[list]:
    """Retrieves list of all FIPs supported by saafe."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {saafe_access_token}",
    }
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="GET",
        endpoint="/User/fip",
        headers=headers,
    )

    if response:
        return response
    logging.error("Failed to get list of FIPs.")
    return None


def discover_accounts(
    phone_number: str,
    fip_id: str,
    fip_types: list[str],
    saafe_access_token: str,
) -> Optional[list]:
    """Discover accounts not yet linked to saafe for given FIP."""
    payload = {
        "FipId": fip_id,
        "Identifiers": [
            {
                "type": "MOBILE",
                "value": f"{phone_number}",
                "categoryType": "STRONG",
            }
        ],
        "FITypes": fip_types,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {saafe_access_token}",
    }

    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="POST",
        endpoint="/User/account/discovery",
        headers=headers,
        payload=payload,
    )

    if response:
        return response
    logging.error(
        (
            f"Failed to get list of accounts from {fip_id=} not yet"
            "linked to saafe."
        )
    )
    return None


def link_accounts(
    discovered_accounts: list,
    signature: str,
    saafe_access_token: str,
    fip_id: str,
) -> Optional[str]:
    """Links account with saafe."""
    payload = {
        "FipId": fip_id,
        "Accounts": discovered_accounts,
        "signature": signature,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {saafe_access_token}",
    }
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="POST",
        endpoint="/User/account/link",
        payload=payload,
        headers=headers,
    )

    if response and "refNumber" in response:
        return response["refNumber"]
    logging.error(f"Failed to link account from {fip_id} with saafe.")
    return None


def account_link_verify_otp(
    ref_number: str,
    otp: str,
    fip_id: str,
    saafe_access_token: str,
) -> Optional[dict]:
    """Verifies OTP for linking account with saafe."""
    payload = {"RefNumber": ref_number, "token": otp, "fipId": fip_id}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {saafe_access_token}",
    }
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="POST",
        endpoint="/User/account/link/verify",
        payload=payload,
        headers=headers,
    )

    if response:
        return response
    logging.error("OTP verification failed while account linking.")
    return None


# Consent APIs


def get_all_consents(saafe_access_token: str) -> Optional[list]:
    """Retrieves list of consents associated with the user account."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {saafe_access_token}",
    }
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="GET",
        endpoint="/User/Consent",
        headers=headers,
    )

    if response:
        return response
    logging.error("Failed to get list of consents.")
    return None


def get_consent_summary(
    consent_handle: str, saafe_access_token: str
) -> Optional[list]:
    """Fetches summary of given consent."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {saafe_access_token}",
    }
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="GET",
        endpoint=f"/User/Consent/handle?consentHandle={consent_handle}",
        headers=headers,
    )

    if response:
        return response[0]
    logging.error(
        "Failed to get summary of consent handle %s." % consent_handle
    )
    return None


def set_consent_state(
    consent_handle: str,
    selected_accounts: str,
    saafe_access_token: str,
    consent_approval_status: str = "READY",
) -> Optional[dict]:
    """Updates the state of consent linked to given handle."""
    payload = {
        "consentHandle": [consent_handle],
        "constentApprovalStatus": consent_approval_status,
        "accounts": selected_accounts,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {saafe_access_token}",
    }
    response = api_utils.make_request(
        base_url=saafe_constants.SAAFE_BASE_URL,
        method="POST",
        endpoint="/User/Consents/Approval/Verification",
        payload=payload,
        headers=headers,
    )

    if response:
        return response
    logging.error(
        "Status changed to %s for consent handle %s."
        % (consent_approval_status, consent_handle)
    )
    return None


# Helper methods


def get_latest_valid_approved_consent(consents: dict) -> Optional[dict]:
    """Gets the latest approved and active consent."""
    today = datetime.datetime.now(
        datetime.timezone.utc
    )  # Current date with UTC timezone info
    valid_consents = []

    for consent in consents["content"]:
        # Check if the consent is approved, active, and valid today
        consent_expiry = datetime.datetime.fromisoformat(
            consent["consentExpiry"].replace("Z", "+00:00")
        )
        if (
            consent.get("consentApprovalStatusType") == "APPROVED"
            and consent.get("consentStatusType") == "ACTIVE"
            and consent_expiry >= today
        ):
            # Add valid consent to the list
            valid_consents.append(consent)

    # Sort valid consents by updatedOn date in descending order to get the
    # latest consent first.
    valid_consents.sort(
        key=lambda x: datetime.datetime.fromisoformat(
            x["updatedOn"].replace("Z", "+00:00")
        ),
        reverse=True,
    )

    # Return the latest valid consent if any
    return valid_consents[0] if valid_consents else None


def get_linked_accounts_wth_enriched_data(
    saafe_access_token: str,
    all_fips: list,
    consent_handle: Optional[str] = None,
) -> Optional[list]:
    """Gets already linked accounts enriched with additional metadata."""
    # Get metadata from all the FIPs.
    fip_metadata = {}
    for fip_type, fip_entities in all_fips.items():
        for fip in fip_entities:
            fip_metadata.update({fip["name"]: {"logoUrl": fip["logoUrl"]}})

    # Get list of accounts already linked to saafe.
    existing_accounts = get_linked_accounts(
        saafe_access_token=saafe_access_token,
        consent_handle=consent_handle,
    )
    if not existing_accounts:
        return None

    # Keep accounts relevant to advisory use case.
    existing_accounts_filtered = []
    for account in existing_accounts:
        if account["fiType"] in saafe_constants.FI_TYPES:
            fip = account["fipName"]
            account.update(fip_metadata[fip])
            existing_accounts_filtered.append(account)

    # Sort by expected FI_TYPES order
    existing_accounts_filtered = sorted(
        existing_accounts_filtered,
        key=lambda x: saafe_constants.FI_TYPES.index(x["fiType"])
        if x["fiType"] in saafe_constants.FI_TYPES
        else len(saafe_constants.FI_TYPES),
    )

    return existing_accounts_filtered
