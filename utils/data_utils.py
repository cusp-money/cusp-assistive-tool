"""Helper library for data interactions."""

import json
import logging
import os

import pandas as pd

from constants import database_constants


def create_local_database():
    """Creates a local database file."""
    os.makedirs(database_constants.DB_DIR, exist_ok=True)
    pd.DataFrame(columns=["client_id", "doc_id"]).to_csv(
        database_constants.DB_FILE, index=False
    )
    logging.info(
        f"Created empty database file at {database_constants.DB_FILE}"
    )


def get_doc_by_phone(phone_number: str) -> str:
    """Gets the google doc id stored against provided phone number."""
    if not os.path.exists(database_constants.DB_FILE):
        logging.warning(
            f"Database file {database_constants.DB_FILE} does not exists."
        )
        create_local_database()
    data = pd.read_csv(database_constants.DB_FILE)
    data["client_id"] = data["client_id"].astype(str)

    # Filter the rows where client_id matches the given mobile number
    result = data[data["client_id"] == str(phone_number)]

    # If a document ID exists for this mobile number, return it; otherwise null
    if not result.empty:
        return result["doc_id"].tolist()[0]
    return ""


def save_locally(phone_number: str, doc_id: str):
    """Saves doc id locally against phone number."""
    if not os.path.exists(database_constants.DB_FILE):
        logging.warning(
            f"Database file {database_constants.DB_FILE} does not exists."
        )
        create_local_database()
    result_db = pd.read_csv(database_constants.DB_FILE)
    result_db["client_id"] = result_db["client_id"].astype(str)

    # Saving doc id in csv locally
    new_index = result_db.shape[0]
    result_db.at[new_index, "client_id"] = str(phone_number)
    result_db.at[new_index, "doc_id"] = doc_id
    result_db.to_csv(database_constants.DB_FILE, index=False)
    logging.info(
        "Added phone number %s to doc %s mapping in %s"
        % (phone_number, doc_id, database_constants.DB_FILE)
    )


def load_json_from_disk(filepath: str):
    """Reads the json from disk."""
    if not os.path.exists(filepath):
        raise ValueError(f"File {filepath} does not exists.")
    with open(filepath, "r") as f:
        data = json.loads(f.read())
    return data
