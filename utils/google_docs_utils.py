"""Helper library to interact with google docs."""

import io
import logging
from typing import Any

from gdoctableapppy import gdoctableapp
from google.oauth2 import service_account
from googleapiclient import discovery, errors, http

from constants import customer_profile_doc


def get_google_doc_creds() -> tuple[any]:
    """Gets the creds for writing to google docs."""
    scopes = [
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = service_account.Credentials.from_service_account_file(
        customer_profile_doc.SERVICE_ACCOUNT_FILEPATH, scopes=scopes
    )
    docs_service = discovery.build("docs", "v1", credentials=creds)
    drive_service = discovery.build("drive", "v3", credentials=creds)
    return creds, docs_service, drive_service


def share_document(drive_service: any, document_id: str, email: str):
    """Share the Google Doc with the specified email as an editor."""
    # Define the permissions
    permissions = {"type": "user", "role": "writer", "emailAddress": email}
    # Use the Drive API to add permissions
    drive_service.permissions().create(
        fileId=document_id, body=permissions, fields="id"
    ).execute()
    logging.info(f"Google doc {document_id} shared with {email}")


def share_document_publicly(
    drive_service: any, document_id: str, role: str = "reader"
):
    """Share the Google Doc publicly with the specified role."""
    # Define the permissions to allow anyone with the link
    permissions = {"type": "anyone", "role": role}
    # Use the Drive API to add permissions
    drive_service.permissions().create(
        fileId=document_id, body=permissions, fields="id"
    ).execute()
    logging.info(f"Google doc {document_id} shared publicly with role {role}")


def get_doc_as_md(doc_id: str, drive_service: any) -> str:
    """Exports given google doc as markdown text."""
    try:
        request = drive_service.files().export_media(
            fileId=doc_id, mimeType="text/markdown"
        )
        file = io.BytesIO()

        downloader = http.MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

    except errors.HttpError as error:
        logging.error(
            f"Error {error} downloading google doc {doc_id} as markdown."
        )
        return ""

    return file.getvalue().decode("utf-8")


def create_new_google_doc(docs_service: any, title: str) -> str:
    """Creates a new google doc with given title."""
    doc = docs_service.documents().create(body={"title": title}).execute()
    document_id = doc.get("documentId")

    logging.info(f"Created new doc with id {document_id}.")
    return document_id


def get_document_length(docs_service: Any, doc_id: str) -> str:
    """Gets the length of the document in terms of character count."""
    doc = docs_service.documents().get(documentId=doc_id).execute()
    return doc.get("body").get("content")[-1].get("endIndex")


def write_heading_to_google_doc(
    doc_id: str, heading: str, docs_service: Any, heading_level: str = "2"
):
    """Writes a heading to the Google Doc."""
    # Get the current document length to insert at the end
    end_index = get_document_length(docs_service=docs_service, doc_id=doc_id)

    # Prepare requests to insert the heading at the end
    requests = [
        {
            "insertText": {
                "location": {
                    "index": end_index - 1  # Insert just before the end
                },
                "text": heading + "\n",
            }
        },
        {
            "updateParagraphStyle": {
                "range": {
                    "startIndex": end_index,
                    "endIndex": end_index + len(heading),
                },
                "paragraphStyle": {
                    "namedStyleType": f"HEADING_{heading_level}"
                },
                "fields": "namedStyleType",
            }
        },
    ]

    # Execute batch update
    docs_service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()
    logging.info(f"Heading '{heading}' added successfully.")


def write_title_to_google_doc(
    doc_id: str,
    title: str,
    docs_service: Any,
):
    """Writes a title to the Google Doc."""
    # Get the current document length to insert at the end
    end_index = get_document_length(docs_service=docs_service, doc_id=doc_id)

    # Prepare requests to insert the title at the end
    requests = [
        {
            "insertText": {
                "location": {
                    "index": end_index - 1  # Insert just before the end
                },
                "text": "\n" + title + "\n",
            }
        }
    ]

    # Execute batch update
    docs_service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()
    logging.info(f"Title '{title}' added successfully.")


def write_table_to_google_doc(
    table_data: list[list[str]], doc_id: str, creds: Any, docs_service: Any
):
    """Writes a table to the Google Doc."""
    # Ensure the table_data is not empty
    if not table_data or not all(isinstance(row, list) for row in table_data):
        raise ValueError(
            "Invalid table data provided. Expected a list of lists."
        )

    # Prepare the table resource
    rows = len(table_data)  # Number of rows in the table
    columns = len(
        table_data[0]
    )  # Number of columns in the table (assumed uniform)

    # Get the current document length to insert at the end
    end_index = get_document_length(docs_service=docs_service, doc_id=doc_id)

    # Create table resource for Google Docs API
    table_resource = {
        "service_account": creds,
        "documentId": doc_id,
        "rows": rows,
        "columns": columns,
        "createIndex": end_index - 1,  # Insert the table at the end
        "values": table_data,
    }

    # Create the table
    res = gdoctableapp.CreateTable(table_resource)
    logging.info("Table Response:", res)
