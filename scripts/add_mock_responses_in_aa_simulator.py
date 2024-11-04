"""Adds mock responses in aa simulator.

Sample command:

python scripts/add_mock_responses_in_aa_simulator.py
"""

import logging

from constants import sahamatinet_constants
from data.mocks import mock_data
from utils import api_utils
from utils.sahamati import sahamati_rahasya_utils, sahamatinet_utils


def add_mock_response_in_aa(mock_response: dict):
    """Adds a mock response for given fi type in mock aa entity."""
    sahamati_user_token = sahamatinet_utils.get_sahamatinet_user_token(
        sahamatinet_user_name=sahamatinet_constants.USER_NAME,
        sahamatinet_password=sahamatinet_constants.PASSWORD,
    )

    # First try to add new response for the scenario
    response = sahamatinet_utils.add_mock_response(
        mock_response_data=mock_response,
        sahamati_user_token=sahamati_user_token,
    )
    if not response:
        # Try to update response if failed
        response = sahamatinet_utils.update_mock_response(
            mock_response_data=mock_response,
            sahamati_user_token=sahamati_user_token,
        )

    return response


def get_mock_response_for_fi_type(fi_type: str):
    """Gets the encrypted mock reponse for given fi type."""
    raw_fi_data = mock_data.dummy_accounts_data.get(fi_type, None)
    if not raw_fi_data:
        raise ValueError(f"No data found for fi_type {fi_type}.")

    encrypted_data = sahamati_rahasya_utils.encrypt_fi_data(
        raw_data=raw_fi_data,
        our_private_key=sahamatinet_constants.AA_SIMULATOR_ECC_KEY_PAIR[
            "privateKey"
        ],
        remote_key_material=sahamatinet_constants.FIU_ECC_KEY_PAIR[
            "KeyMaterials"
        ],
        our_nonce=sahamatinet_constants.AA_SIMULATOR_NONCE,
        remote_nonce=sahamatinet_constants.FIU_NONCE,
    )

    # Verify that we get the same message back
    decrypted_data = sahamati_rahasya_utils.decrypt_fi_data(
        encrypted_data=encrypted_data,
        our_private_key=sahamatinet_constants.FIU_ECC_KEY_PAIR["privateKey"],
        remote_key_material=sahamatinet_constants.AA_SIMULATOR_ECC_KEY_PAIR[
            "KeyMaterials"
        ],
        our_nonce=sahamatinet_constants.FIU_NONCE,
        remote_nonce=sahamatinet_constants.AA_SIMULATOR_NONCE,
    )

    assert raw_fi_data == decrypted_data

    key_material = sahamatinet_constants.AA_SIMULATOR_ECC_KEY_PAIR[
        "KeyMaterials"
    ]
    key_material["Nonce"] = sahamatinet_constants.AA_SIMULATOR_NONCE
    mock_response = {
        "entityId": sahamatinet_constants.MOCK_AA_SIMULATOR,
        "endpoint": "/FI/fetch",
        "scenario": f"{fi_type}_OK",
        "responseCode": 200,
        "response": {
            "ver": "2.0.0",
            "timestamp": api_utils.get_current_utc_time(),
            "txnid": api_utils.generate_transaction_id(),
            "FI": [
                {
                    "fipID": "NOT_REQUIRED_AS_MOCKED",
                    "data": [
                        {
                            "linkRefNumber": "XXXX-XXXX-XXXX",
                            "maskedAccNumber": "XXXXXXXXXXX",
                            "encryptedFI": encrypted_data,
                        }
                    ],
                    "KeyMaterial": key_material,
                }
            ],
        },
    }

    return mock_response


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    for fi_type in mock_data.dummy_accounts_data:
        mock_response = get_mock_response_for_fi_type(fi_type=fi_type)
        response = add_mock_response_in_aa(mock_response=mock_response)
        if not response:
            logging.info(f"Adding mock response for {fi_type} failed.")
            continue
        logging.info(f"Added mock response for {fi_type} successfully.")
