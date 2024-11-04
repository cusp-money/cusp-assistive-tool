"""Streamlit page shown to the user before login providing insights of Cusp."""

import streamlit as st

from constants import onboarding_flow_constants


def show_cusp_info():
    """Displays an informational page about Cusp Money for before login."""
    # Introduction & USP
    st.write(
        (
            "**Cusp Money** connects you with Registered Investment Advisors "
            "who provide personalized financial advice in your preferred "
            "regional language. Our process is secure and tailored to your "
            "needs."
        )
    )

    # How It Works (Condensed)
    st.subheader("How It Works?")
    st.write(
        (
            "1. **Secure Data Sharing**: Share your financial data through an "
            "RBI-registered account aggregator."
            "\n"
            "2. **Personalized Interaction**: Have a 1:1 conversation with our"
            " CuspAI voice assistant to help advisors understand your needs "
            "closely."
            "\n"
            "3. **Expert Advice**: Our RIA uses your data and conversation "
            "insights to provide you with customized advice."
            "\n"
            "4. **Ongoing Support:** If you have questions or wish to discuss "
            "the advice, you can connect with **CuspAI** again for further "
            "clarification – as many times as needed."
        )
    )

    # Call to Action
    st.subheader("Get Started!")
    st.write(
        (
            "To begin, please enter the phone number linked to your "
            "financial accounts in the login form on the left."
            "\n"
            "\n"
            "If you have questions, reach us at 📞 **%s**."
            % (onboarding_flow_constants.CUSP_PHONE_NUMBER)
        )
    )

    # Thank You Message
    st.write("Thank you for choosing Cusp Money as your financial partner.")
