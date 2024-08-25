recovery_template = \
"""From: {from_email}
To: {to_email}
Subject: {subject}

This is your password recovery link, click on it or copy and paste it in your browser to reset your password.

{content}

This link will expire in 20 minutes.
"""

def process_template(from_email: str, to_email: str, subject: str, content: str) -> str:
    return recovery_template.format(from_email=from_email, to_email=to_email, subject=subject, content=content)