import os
from unittest.mock import patch, MagicMock

import alerts


def _set_env():
    os.environ['SMTP_HOST'] = 'smtp.test'
    os.environ['SMTP_PORT'] = '587'
    os.environ['SMTP_USER'] = 'user@test.com'
    os.environ['SMTP_PASSWORD'] = 'secret'
    os.environ['ALERT_TO'] = 'recipient@test.com'


@patch('smtplib.SMTP')
def test_maybe_send_email_env(mock_smtp):
    """Ensure _maybe_send_email sends a message using the SMTP client when env vars set."""
    _set_env()
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    # Call internal helper directly with sample data
    alerts._maybe_send_email(device='TestDevice', packets=42, risk='HIGH', timestamp='2025-12-29 00:00:00')

    assert mock_server.send_message.called, "Expected send_message to be called on the SMTP server"
