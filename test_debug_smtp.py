#!/usr/bin/env python3
"""
Quick test to verify the debug SMTP server works correctly
and can receive emails from the intrusion detector app.
"""

import smtplib
from email.message import EmailMessage


def test_send_to_debug_server():
    """Test sending an email to the local debug SMTP server."""
    
    print("Testing connection to local debug SMTP server...")
    print("Make sure to run: python debug_smtp_server.py in another terminal\n")
    
    try:
        msg = EmailMessage()
        msg["From"] = "alerts@intrusion-detector"
        msg["To"] = "test@example.com"
        msg["Subject"] = "[HIGH] Intrusion alert — Device_1"
        msg.set_content(
            "Time: 2025-12-29 10:30:00\n"
            "Device: Device_1\n"
            "Packets: 500\n"
            "Risk: HIGH\n"
            "RiskScore: 85\n"
            "Explanation: Unusually high packet transmission; Sudden deviation from device baseline\n"
            "\n"
            "This is a test alert from Smart Home Intrusion Detector."
        )
        
        with smtplib.SMTP('localhost', 1025, timeout=5) as server:
            server.send_message(msg)
        
        print("✅ Test email sent successfully!")
        print("   Check the debug_smtp_server.py terminal to see the email printed.")
        return True
        
    except ConnectionRefusedError:
        print("❌ Could not connect to localhost:1025")
        print("   Make sure you have run: python debug_smtp_server.py")
        return False
    except OSError as e:
        print(f"❌ Network error: {e}")
        print("   Check that the debug SMTP server is running.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    success = test_send_to_debug_server()
    exit(0 if success else 1)
