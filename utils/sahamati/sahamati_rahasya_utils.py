"""Utilities to encrypt and decrypt fi messages using sahamati rahasya APIs.

Based on https://github.com/Sahamati/rahasya.
"""

import base64
import logging
import secrets
from typing import Optional

from constants import sahamati_rahasya_constants
from utils import api_utils

# Sahamati Rahasya APIs


def generate_ecc_key_pair() -> Optional[dict]:
    """Generates ECC key pair."""
    response = api_utils.make_request(
        base_url=sahamati_rahasya_constants.HOST,
        method="GET",
        endpoint="/ecc/v1/generateKey",
    )

    if response:
        return response
    logging.error("Failed to generate ecc key pair.")
    return None


def encrypt_fi_data(
    raw_data: str,
    our_private_key: str,
    remote_key_material: dict,
    our_nonce: str,
    remote_nonce: str,
) -> Optional[str]:
    """Encrypts FI data using shared key generated using provided key pair."""
    # Encode the raw_data using b64 encoding
    b64_data = base64.b64encode(raw_data.encode()).decode()

    payload = {
        "base64Data": b64_data,
        "base64RemoteNonce": remote_nonce,
        "base64YourNonce": our_nonce,
        "ourPrivateKey": our_private_key,
        "remoteKeyMaterial": remote_key_material,
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    response = api_utils.make_request(
        base_url=sahamati_rahasya_constants.HOST,
        method="POST",
        endpoint="/ecc/v1/encrypt",
        headers=headers,
        payload=payload,
    )

    if response and "base64Data" in response:
        return response["base64Data"]
    logging.error("Failed to encrypt data.")
    return None


def decrypt_fi_data(
    encrypted_data: str,
    our_private_key: str,
    remote_key_material: dict,
    our_nonce: str,
    remote_nonce: str,
) -> Optional[str]:
    """Decrypts FI data using shared key generated using provided key pair."""
    payload = {
        "base64Data": encrypted_data,
        "base64RemoteNonce": remote_nonce,
        "base64YourNonce": our_nonce,
        "ourPrivateKey": our_private_key,
        "remoteKeyMaterial": remote_key_material,
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    response = api_utils.make_request(
        base_url=sahamati_rahasya_constants.HOST,
        method="POST",
        endpoint="/ecc/v1/decrypt",
        headers=headers,
        payload=payload,
    )

    if response and "base64Data" in response:
        # Step 1: get the decrypted b64 string.
        decrypted_fi_data_b64 = response["base64Data"]
        decrypted_fi_data_encoded = base64.b64decode(
            decrypted_fi_data_b64
        ).decode()

        # Step 2: Decode the b64 string to get the original message.
        decrypted_fi_data_raw = base64.b64decode(
            decrypted_fi_data_encoded
        ).decode()
        return decrypted_fi_data_raw
    logging.error("Failed to encrypt data.")
    return None


# Helper methods


def generate_random_base64_nonce():
    """Generates random base64 nonce."""
    # Generate a 32-byte secure random nonce
    nonce = secrets.token_bytes(32)
    # Encode the nonce in base64
    nonce_base64 = base64.b64encode(nonce).decode("utf-8")
    return nonce_base64


def get_public_private_key_pair_for_fi_request() -> Optional[tuple]:
    """Gets a new public private key pair for fi request."""
    our_ecc_key_pair = generate_ecc_key_pair()
    if not our_ecc_key_pair:
        return None
    our_nonce = generate_random_base64_nonce()

    our_private_key = our_ecc_key_pair["privateKey"]
    our_public_key_material = our_ecc_key_pair[
        "KeyMaterials"
    ]  # Our public key

    our_public_key_material["Nonce"] = our_nonce
    our_public_key_material["curve"] = our_public_key_material[
        "curve"
    ].capitalize()  # Due to mismatch in rahasya api and sahamati api

    return our_nonce, our_private_key, our_public_key_material
