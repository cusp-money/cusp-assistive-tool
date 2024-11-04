"""Helper library to consume SahamatiNet APIs."""

import logging
from typing import Optional

import requests

from constants import sahamatinet_constants
from utils import api_utils
from utils.sahamati import sahamati_rahasya_utils

# Token Service [IAM]


def get_sahamatinet_user_token(
    sahamatinet_user_name: str, sahamatinet_password: str
) -> Optional[str]:
    """Generates sahamatinet user token."""
    payload = "username=%s&password=%s" % (
        requests.utils.quote(sahamatinet_user_name),
        requests.utils.quote(sahamatinet_password),
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="POST",
        endpoint="/iam/v1/user/token/generate",
        payload=payload,
        headers=headers,
    )

    if response and "accessToken" in response:
        return response["accessToken"]
    logging.error("Could not get sahamatinet user token.")
    return None


def get_sahamatinet_member_secret(
    sahamatinet_member_id: str, sahamatinet_user_token: str
) -> Optional[str]:
    """Generates sahamatinet member secret."""
    payload = {
        "entityId": sahamatinet_member_id,
        "txnId": api_utils.generate_transaction_id(),
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sahamatinet_user_token}",
    }
    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="POST",
        endpoint="/iam/v1/entity/secret/read",
        payload=payload,
        headers=headers,
    )

    if response and "secret" in response:
        return response["secret"]
    logging.error("Could not get sahamatinet member secret.")
    return None


def get_sahamatinet_member_token(
    sahamatinet_member_id: str, sahamatinet_member_secret: str
) -> Optional[str]:
    """Generates sahamatinet member token."""
    payload = "id=%s&secret=%s" % (
        requests.utils.quote(sahamatinet_member_id),
        requests.utils.quote(sahamatinet_member_secret),
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="POST",
        endpoint="/iam/v1/entity/token/generate",
        payload=payload,
        headers=headers,
    )

    if response and "accessToken" in response:
        return response["accessToken"]
    logging.error("Could not get sahamatinet member token.")
    return None


# Proxy API - Sandbox (FIU -> AA)


def create_consent(
    phone_number: str,
    fi_types: list[str],
    sahamatinet_member_token: str,
    sahamatinet_member_id: str,
) -> Optional[str]:
    """Creates a consent request and returns consent handle."""
    current_time = api_utils.get_current_utc_time()
    payload = {
        "ver": "2.0.0",
        "timestamp": current_time,
        "txnid": api_utils.generate_transaction_id(),
        "ConsentDetail": {
            "consentStart": current_time,
            "consentExpiry": api_utils.get_current_utc_plus_one_day(),
            "consentMode": "VIEW",
            "fetchType": "PERIODIC",
            "consentTypes": [
                "PROFILE",
                "SUMMARY",
                "TRANSACTIONS",
            ],
            "fiTypes": fi_types,
            "DataConsumer": {
                "id": sahamatinet_member_id,
                "type": "FIU",
            },
            "Customer": {
                "id": f"{phone_number}@saafe-sandbox",
                "Identifiers": [{"type": "MOBILE", "value": phone_number}],
            },
            "Purpose": {
                "code": "101",
                "refUri": "https://api.rebit.org.in/aa/purpose/101.xml",
                "text": "Wealth management service",
                "Category": {"type": "Personal Finance"},
            },
            "FIDataRange": {
                "from": "2023-12-06T11:39:57.153Z",
                "to": current_time,
            },
            "DataLife": {"unit": "DAY", "value": 1},
            "Frequency": {"unit": "DAY", "value": 100},
        },
    }
    headers = {
        "x-jws-signature": api_utils.get_detached_jws(
            payload=payload,
            private_key=sahamatinet_constants.RSA_PRIVATE_KEY_JWK,
        ),
        "Content-Type": "application/json",
        "x-request-meta": api_utils.dict_to_b64(
            data={"recipient-id": "saafe-sandbox"}
        ),
        "client_api_key": sahamatinet_member_token,
    }
    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="POST",
        endpoint="/proxy/v2/Consent",
        payload=payload,
        headers=headers,
    )

    if response and "ConsentHandle" in response:
        return response["ConsentHandle"]
    logging.error("Could not create a new consent handle.")
    return None


def fetch_consent(
    consent_id: str, sahamatinet_member_token: str
) -> Optional[str]:
    """Fetches signed consent for the given consent id."""
    payload = {
        "ver": "2.0.0",
        "timestamp": api_utils.get_current_utc_time(),
        "txnid": api_utils.generate_transaction_id(),
        "consentId": consent_id,
    }
    headers = {
        "x-jws-signature": api_utils.get_detached_jws(
            payload=payload,
            private_key=sahamatinet_constants.RSA_PRIVATE_KEY_JWK,
        ),
        "Content-Type": "application/json",
        "x-request-meta": api_utils.dict_to_b64(
            data={"recipient-id": "saafe-sandbox"}
        ),
        "client_api_key": sahamatinet_member_token,
    }

    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="POST",
        endpoint="/proxy/v2/Consent/fetch",
        payload=payload,
        headers=headers,
    )

    if response and "signedConsent" in response:
        return response["signedConsent"]
    logging.error(
        "Could not fetch signed consent for consent id %s" % consent_id
    )
    return None


def create_fi_request(
    consent_id: str,
    signed_consent: str,
    sahamatinet_member_token: str,
    start_date: str,
    end_date: str,
) -> Optional[str]:
    """Creates a new FI request for given signed consent id.

    It also returns the private nonce and private key for decrypting data.
    """
    # Generate public private key pair for e2e encrypted data fetching.
    public_private_key_pair = (
        sahamati_rahasya_utils.get_public_private_key_pair_for_fi_request()
    )
    if not public_private_key_pair:
        return None
    our_nonce, our_private_key, our_public_key_material = (
        public_private_key_pair
    )

    payload = {
        "ver": "2.0.0",
        "timestamp": api_utils.get_current_utc_time(),
        "txnid": api_utils.generate_transaction_id(),
        "FIDataRange": {
            "from": start_date,
            "to": end_date,
        },
        "Consent": {
            "id": consent_id,
            "digitalSignature": signed_consent.split(".")[-1],
        },
        "KeyMaterial": our_public_key_material,
    }

    headers = {
        "x-jws-signature": api_utils.get_detached_jws(
            payload=payload,
            private_key=sahamatinet_constants.RSA_PRIVATE_KEY_JWK,
        ),
        "Content-Type": "application/json",
        "x-request-meta": api_utils.dict_to_b64(
            data={"recipient-id": "saafe-sandbox"}
        ),
        "client_api_key": sahamatinet_member_token,
    }

    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="POST",
        endpoint="/proxy/v2/FI/request",
        payload=payload,
        headers=headers,
    )

    if response and "sessionId" in response:
        return response["sessionId"], our_nonce, our_private_key
    logging.error("Could not get session id for consent id : %s" % consent_id)
    return None


def fi_fetch(
    accounts: list,
    fip_id: str,
    session_id: str,
    sahamatinet_member_token: str,
    mock_params: dict = {},
) -> Optional[dict]:
    """Fetches data if available for given session id."""
    payload = {
        "ver": "2.0.0",
        "timestamp": api_utils.get_current_utc_time(),
        "txnid": api_utils.generate_transaction_id(),
        "sessionId": session_id,
        "fipId": fip_id,
        "linkRefNumber": [{"id": link_ref_num} for link_ref_num in accounts],
    }
    headers = {
        "x-jws-signature": api_utils.get_detached_jws(
            payload=payload,
            private_key=sahamatinet_constants.RSA_PRIVATE_KEY_JWK,
        ),
        "Content-Type": "application/json",
        "x-scenario-id": mock_params.get("x-scenario-id", "Ok"),
        "x-request-meta": api_utils.dict_to_b64(
            data={
                "recipient-id": mock_params.get(
                    "recipient-id", "saafe-sandbox"
                )
            }
        ),
        "client_api_key": sahamatinet_member_token,
    }

    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="POST",
        endpoint="/proxy/v2/FI/fetch",
        payload=payload,
        headers=headers,
    )

    if response:
        return response
    logging.error("Could not fetch data for session id %s" % session_id)
    return None


# Simulator


def add_mock_response(
    mock_response_data: dict, sahamati_user_token: str
) -> Optional[dict]:
    """Adds a mock response for scenario and entity mentioned in payload."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sahamati_user_token}",
    }

    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="POST",
        endpoint="/simulate/v2/response/add",
        payload=mock_response_data,
        headers=headers,
    )

    if response:
        return response
    logging.error("Could not add a mock response.")
    return None


def update_mock_response(
    mock_response_data: dict, sahamati_user_token: str
) -> Optional[dict]:
    """Updates a mock response for scenario and entity mentioned in payload."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sahamati_user_token}",
    }

    response = api_utils.make_request(
        base_url=sahamatinet_constants.HOST,
        method="PUT",
        endpoint="/simulate/v2/response/update",
        payload=mock_response_data,
        headers=headers,
    )

    if response:
        return response
    logging.error("Could not update a mock response.")
    return None
