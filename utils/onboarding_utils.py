"""Helper library for user onboarding journey."""

import enum

from constants import customer_profile_doc
from utils import data_utils, google_docs_utils


class UserJourneyStage(enum.Enum):
    """User journey stages during onboarding."""

    AA_DATA_PENDING = 1  # User is yet to provide consent for data sharing.
    CUSTOMER_PROFILE_PENDING = 2  # Initial 1:1 call with AI is pending.
    ADVICE_GENERATION_PENDING = 3  # Advisor yet to add advise.
    ADVICE_EXISTS = 4  # User journey completed, can inquire about advise.


def check_advice_presence(text: str) -> bool:
    """Checks if advisor has already provided the advise or not."""
    matching_keyword = customer_profile_doc.FINANCIAL_ADVISE_DESCRIPTION
    if matching_keyword not in text:
        return False
    advice_str = text.split(matching_keyword)[1].strip()
    return bool(advice_str)


def detect_user_journey_state(phone_number: str) -> UserJourneyStage:
    """Detects the current user journey stage for a registered used."""
    # Check if data has already been analyzed
    doc_id = data_utils.get_doc_by_phone(phone_number=phone_number)
    if not doc_id:
        return UserJourneyStage.AA_DATA_PENDING

    # Get creds to access google doc
    _, _, drive_service = google_docs_utils.get_google_doc_creds()

    markdown_content = google_docs_utils.get_doc_as_md(
        doc_id=doc_id, drive_service=drive_service
    )
    if check_advice_presence(text=markdown_content):
        return UserJourneyStage.ADVICE_EXISTS

    if (
        customer_profile_doc.CUSTOMER_PROFILE_DESCRIPTION
        not in markdown_content
    ):
        return UserJourneyStage.CUSTOMER_PROFILE_PENDING

    return UserJourneyStage.ADVICE_GENERATION_PENDING
