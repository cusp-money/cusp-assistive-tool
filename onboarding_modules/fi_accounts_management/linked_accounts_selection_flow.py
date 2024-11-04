"""Submodule to handle linked account selection for consent approval."""

from typing import Optional

import num2words
import streamlit as st


def show_linked_accounts_with_checkboxes(
    linked_accounts: list,
) -> Optional[list]:
    """Shows linked accounts and allows selection for consent approval."""
    with st.status(
        label="Fetching already linked accounts...", expanded=True
    ) as status:
        if not linked_accounts:
            st.header("No existing accounts are linked yet")
            st.markdown(
                "You can link the ones which are found earlier if any."
            )
            status.update(
                label="Existing accounts discovery complete",
                state="complete",
                expanded=True,
            )
            return

        num_acc = len(linked_accounts)
        st.header(
            "%s account%s %s ready to share"
            % (
                num2words.num2words(num_acc).capitalize(),
                "s" if num_acc > 1 else "",
                "are" if num_acc > 1 else "is",
            )
        )
        st.markdown("Give your consent for analyzing selected accounts:")

        # Initialize selected accounts in session state
        if "selected_accounts" not in st.session_state:
            st.session_state.selected_accounts = set()

        # Displaying linked accounts
        st.markdown("- Your data will be fetched only once.")
        st.markdown(
            "- It will be deleted as soon as the summary is generated."
        )
        st.markdown("- Without revealing any personal information.")
        st.markdown("### Choose accounts to share")

        for account in linked_accounts:
            col1, col2, col3 = st.columns([0.4, 3, 1])  # Create three columns
            with col1:
                st.image(account["logoUrl"], width=55)  # Logo
            with col2:
                # Account identifiers such as provider name and masked acc no.
                st.markdown(
                    "**%s** (%s)"
                    % (
                        account["fipName"],
                        account["fiType"].replace("_", " ").capitalize(),
                    )
                )
                st.markdown(account["maskedAccNumber"])
            with col3:
                # Checkbox for selecting the account
                checkbox = st.checkbox(
                    label="Select",
                    key=account["linkRefNumber"],
                    value=account["linkRefNumber"]
                    in st.session_state.selected_accounts,
                )
                if checkbox:
                    st.session_state.selected_accounts.add(
                        account["linkRefNumber"]
                    )
                else:
                    if (
                        account["linkRefNumber"]
                        in st.session_state.selected_accounts
                    ):
                        st.session_state.selected_accounts.discard(
                            account["linkRefNumber"]
                        )

        status.update(
            label="Existing accounts fetched", state="complete", expanded=True
        )
