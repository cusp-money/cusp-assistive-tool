"""Helper library for API handling."""

import base64
import datetime
import json
import logging
import time
import uuid
from typing import Any, Optional

import requests
from joserfc.jwk import RSAKey
from joserfc.rfc7797 import serialize_compact


def make_request(
    base_url: str,
    method: str,
    endpoint: str,
    headers: Optional[dict[str, str]] = None,
    payload: Optional[dict[str, Any]] = None,
    files: Optional[dict[str, Any]] = None,
    retries: int = 3,
) -> Optional[dict[str, Any]]:
    """Handles API requests."""
    url = f"{base_url}{endpoint}"
    headers = headers or {"Content-Type": "application/json"}

    if isinstance(payload, dict):
        payload = (
            json.dumps(payload, separators=(",", ":")) if payload else None
        )

    for attempt in range(retries):
        start_time = time.time()  # Start timing the request
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                data=payload,
                files=files,
            )
            duration = (time.time() - start_time) * 1000  # ms

            if response.ok:
                logging.info(f"Successfully called {url} in {duration:.2f} ms")
                return response.json()  # Success case

            # Log non-2xx response but avoid raising an exception immediately
            logging.error(
                "Req. failed code=%d, attempt=%d for %s, error %s in %.2f ms"
                % (
                    response.status_code,
                    attempt + 1,
                    url,
                    response.text,
                    duration,
                )
            )

        except requests.RequestException as e:
            duration = (time.time() - start_time) * 1000  # ms
            logging.error(
                "Request exception on attempt %d in %.2f ms: %s"
                % (attempt + 1, duration, str(e))
            )

    logging.error("All attempts failed.")
    return None  # None returned in case all attempts fail


def generate_transaction_id() -> str:
    """Generates a random transaction id."""
    return str(uuid.uuid4())


def get_current_utc_time() -> str:
    """Gets current UTC timestamp."""
    return (
        datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )[:-3]
        + "Z"
    )


def get_current_utc_plus_one_day() -> str:
    """Gets current UTC timestamp plus one day."""
    next_day = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(days=1)
    return next_day.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def dict_to_b64(data: dict):
    """Converts dict to base64 string."""
    data = json.dumps(data)
    return base64.b64encode(data.encode()).decode()


def get_detached_jws(payload: dict, private_key: dict) -> str:
    """Generates `x-jws-signature` for given payload."""
    # Private Key
    private_key = RSAKey.import_key(private_key)

    # Headers
    protected = {
        "alg": private_key.alg,
        "kid": private_key.kid,
        "b64": False,
        "crit": ["b64"],
    }

    if isinstance(payload, dict):
        payload = (
            json.dumps(payload, separators=(",", ":")) if payload else None
        )
    # Detached JWS Creation
    value = serialize_compact(
        protected=protected, payload=payload, private_key=private_key
    )

    return value
