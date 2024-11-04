"""Constants used in customer profile google doc."""

DOC_TITLE_PREFIX = "Cusp Money Client"

ADVISOR_EMAIL = "hetul@infocusp.com"

AA_SUMMARY_HEADING = "Account Aggregator Summary"

AA_SUMMARY_DESCRIPTION = (
    "This summary has been generated based on account data provided by the "
    "user through a trusted Account Aggregator. It offers a clear overview of "
    "the user's current bank balances, policies, and financial holdings."
)


CUSTOMER_PROFILE_HEADING = "Customer Profile"

CUSTOMER_PROFILE_DESCRIPTION = (
    "The below information is gathered from the "
    "customer to better understand his financial goals and risk appetite."
)

FINANCIAL_ADVISE_HEADING = "Financial Advice"

FINANCIAL_ADVISE_DESCRIPTION = (
    "Based on the customer profile provided, here's a personalized financial "
    "advice section that aligns with the customer's financial goals, income, "
    "and risk appetite:"
)

# Service account credentials for accessing google doc.
SERVICE_ACCOUNT_FILEPATH = "data/secrets/google_doc_service_account.json"
