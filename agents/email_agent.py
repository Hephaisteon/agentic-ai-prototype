###############
# Email Agent #
###############

import os
import smtplib
from email.message import EmailMessage
from typing import TypedDict

# Define the state structure for the email agent
class EmailAgentState(TypedDict):
    recipient: str
    subject: str
    body: str
    done: bool


def email_agent(state: EmailAgentState) -> EmailAgentState:

    """
    This function sends an email using SMTP based on the provided state.
    If the email is sent successfully, it updates the state to mark 'done' as True.
    """

    # Read credentials from environment variables
    sender_email = os.getenv("email_address")
    sender_password = os.getenv("email_password")

    if not sender_email or not sender_password:
        raise RuntimeError(
            "Email credentials not found. "
            "Please set sender email address and sender email password as environment variables."
        )

    # Create the email message
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = state["recipient"]
    msg["Subject"] = state["subject"]
    msg.set_content(state["body"])

    # Send the email via SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    # Update state and mark as done
    return {
        **state,
        "done": True,
    }