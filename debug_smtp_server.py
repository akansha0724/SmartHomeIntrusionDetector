#!/usr/bin/env python3
"""
Local SMTP Debug Server

Runs a local SMTP server on localhost:1025 that prints all emails to console
instead of sending them over the network. Useful for testing email alerts
without needing real SMTP credentials or internet connectivity.

Usage:
    python debug_smtp_server.py

Then in the Streamlit app:
    SMTP Host: localhost
    SMTP Port: 1025
    SMTP User: (leave blank)
    SMTP Password: (leave blank)
    Alert To: test@example.com
"""

import asyncore
import smtpd
import sys


class DebuggingServer(smtpd.SMTPServer):
    """SMTP server that prints all received emails to console."""

    def process_message(self, peer, mailfrom, rcpttos, data):
        print(f"\n{'='*60}")
        print(f"SMTP Alert Email Received")
        print(f"{'='*60}")
        print(f"From: {mailfrom}")
        print(f"To: {', '.join(rcpttos)}")
        print(f"Peer: {peer}")
        print(f"{'='*60}")
        print(data.decode('utf-8'))
        print(f"{'='*60}\n")


if __name__ == '__main__':
    print("🔧 Starting local SMTP debug server on localhost:1025...")
    print("   In Streamlit app, use:")
    print("   - SMTP Host: localhost")
    print("   - SMTP Port: 1025")
    print("   - SMTP User: (leave blank)")
    print("   - SMTP Password: (leave blank)")
    print("\n📧 Emails will be printed to console instead of sent.\n")
    print("Press Ctrl+C to stop server.\n")

    try:
        server = DebuggingServer(("localhost", 1025), None)
        asyncore.loop()
    except KeyboardInterrupt:
        print("\n✅ Server stopped.")
        sys.exit(0)
    except OSError as e:
        print(f"❌ Error: {e}")
        print("   Port 1025 may already be in use. Try a different port or kill the existing process.")
        sys.exit(1)
