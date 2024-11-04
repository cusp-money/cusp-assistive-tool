"""Streamlit page suggesting the user about pending advice."""

import streamlit as st

from constants import onboarding_flow_constants


def suggest_user_about_advice_pending():
    """Suggests the user about pending advice."""
    # Page Title
    st.subheader("Your Financial Insights Are Being Prepared! 💼")

    # Main Message
    st.write(
        "Thank you for sharing more about your financial goals and family "
        "during the recent conversation. Our Registered Investment Advisor "
        "(RIA) is now carefully reviewing your information to create a "
        "customized plan tailored just for you."
    )

    # Setting Expectations
    st.subheader("What to Expect Next:")
    st.write(
        (
            "Once your advice is ready, we will notify you here. In the "
            "meantime, if you have any questions or need assistance, please "
            "feel free to reach out."
        )
    )

    # Contact Information (if they need assistance)
    st.markdown("### 📞 Need Assistance?")
    st.write("If you have questions, feel free to contact us at:")
    st.markdown("## **%s**" % (onboarding_flow_constants.CUSP_PHONE_NUMBER))

    # Thank You Message
    st.write(
        (
            "Thank you for your patience as we work to deliver guidance "
            "that fits your goals perfectly."
        )
    )
