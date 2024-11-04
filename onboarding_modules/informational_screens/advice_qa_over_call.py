"""Streamlit page suggesting the user to call Cusp AI for Q&A over advice."""

import streamlit as st

from constants import onboarding_flow_constants


def call_cusp_ai_for_qa_over_advise():
    """Suggests the user to call Cusp AI for Q&A over advice."""
    # Page Title
    st.subheader("Your Personalized Financial Advice is Ready! 📈")

    # Main Message
    st.write(
        (
            "Thank you for trusting us throughout this journey. Based on the "
            "financial information you shared and our recent conversation, "
            "our Registered Investment Advisor (RIA) has crafted detailed, "
            "customized advice just for you."
        )
    )

    # Invitation to Discuss Advice
    st.subheader("Have Questions About Your Advice?")
    st.write("Our AI is ready to assist you! Just call:")
    st.markdown("## 📞 **%s**" % (onboarding_flow_constants.CUSP_PHONE_NUMBER))
    st.write(
        (
            "to have a conversation with Cusp AI. You can ask as many "
            "questions as you’d like about the advice—whether it's about "
            " specific recommendations, future steps, or clarifying any "
            "detail."
        )
    )

    # Long-term Availability Message
    st.subheader("The Best Part? Cusp AI is Always Here for You.")
    st.write(
        (
            "We understand that financial plans evolve. So even if it's "
            "a year, two years, or even three years down the road, you can "
            "call us again. We’ll be here to help ensure you’re on track, "
            "every step of the way."
        )
    )
