"""Streamlit page suggesting user to call Cusp AI for 1st 1:1 conversation."""

import streamlit as st

from constants import onboarding_flow_constants


def suggest_user_to_call_cusp_ai_agent():
    """Suggests user to call Cusp AI agent for 1:1 conversation."""
    # Main Message
    st.subheader("Great News!")
    st.write(
        (
            "We've analyzed your financial data and prepared a preliminary "
            "summary. Now, to provide the most accurate and personalized "
            "financial guidance, our AI would like to have a brief, 1:1 "
            "conversation with you."
        )
    )

    # Additional Explanation
    st.write(
        (
            "In this call, the AI will ask a few additional questions "
            "about your goals, family, and other factors that don't appear "
            "directly on your statements. This helps us ensure that the "
            "insights we provide are uniquely tailored to your life situation."
        )
    )
    st.write(
        (
            "Once complete, our Registered Investment Advisor (RIA) will "
            "review this summary and develop recommendations just for you."
        )
    )

    # Call to Action
    st.markdown("### Ready to Continue?")
    st.write("Simply call:")
    st.markdown("## 📞 **%s**" % (onboarding_flow_constants.CUSP_PHONE_NUMBER))
    st.write(
        (
            "Start your secure, private AI conversation and get closer to "
            "your financial goals!"
        )
    )
