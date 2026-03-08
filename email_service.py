import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

# Attempt to load secrets from Streamlit Cloud (`st.secrets`) when available,
# otherwise fall back to environment variables loaded from `.env`.
_secrets = {}
try:
    import streamlit as st
    _secrets = getattr(st, "secrets", {}) or {}
except Exception:
    _secrets = {}

def _get_secret(key: str, default: str = "") -> str:
    return os.getenv(key) or _secrets.get(key) or default

SENDER_EMAIL = _get_secret("SENDER_EMAIL", "")
SENDER_PASSWORD = _get_secret("SENDER_PASSWORD", "")
SENDER_NAME = _get_secret("SENDER_NAME", "SuRe Newsletter")
SMTP_SERVER = _get_secret("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(_get_secret("SMTP_PORT", "587"))

def send_welcome_email(subscriber_name: str, subscriber_email: str) -> Dict:
    """Send a welcome email to new subscribers"""
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return {
            "success": False,
            "error": "Email credentials not configured. Please set SENDER_EMAIL and SENDER_PASSWORD in .env"
        }
    
    try:
        # Create email message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome to SuRe Newsletter! 📰"
        message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message["To"] = subscriber_email
        
        # Plain text version
        text = f"""
Hi {subscriber_name},

Welcome to SuRe Newsletter! 🎉

You're now part of our growing community of readers who appreciate curated, reliable insights delivered weekly.

What to expect:
- Thoughtful, well-researched content
- Practical insights you can use
- Weekly delivery every week
- Community of like-minded readers

This week's issue is already waiting for you. Feel free to browse our archive or wait for the next one!

Stay curious!
SuRe Team
"""
        
        # HTML version
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <!-- Header -->
                    <div style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid #1E3A8A; padding-bottom: 20px;">
                        <h1 style="color: #1E3A8A; margin: 0; font-size: 32px;">📰 SuRe</h1>
                        <p style="color: #64748B; margin: 5px 0 0 0;">Thoughtful & Curated Tech</p>
                    </div>
                    
                    <!-- Welcome message -->
                    <div style="margin-bottom: 30px;">
                        <h2 style="color: #1E3A8A; font-size: 24px;">Welcome, {subscriber_name}! 🎉</h2>
                        <p style="font-size: 16px;">You're now part of our growing community of readers who appreciate curated, reliable insights delivered weekly.</p>
                    </div>
                    
                    <!-- What to expect -->
                    <div style="background: #F0F9FF; border-left: 4px solid #1E3A8A; padding: 20px; margin-bottom: 30px; border-radius: 8px;">
                        <h3 style="color: #1E3A8A; margin-top: 0;">What to Expect</h3>
                        <ul style="color: #475569;">
                            <li>🎯 Thoughtful, well-researched content</li>
                            <li>💡 Practical insights you can use</li>
                            <li>📬 Weekly delivery every week</li>
                            <li>👥 Community of like-minded readers</li>
                        </ul>
                    </div>
                    
                    <!-- CTA -->
                    <div style="text-align: center; margin-bottom: 30px;">
                        <p style="font-size: 16px; color: #475569;">Our latest issue is ready for you to explore!</p>
                    </div>
                    
                    <!-- Footer -->
                    <div style="border-top: 1px solid #E2E8F0; padding-top: 20px; text-align: center; color: #94A3B8; font-size: 12px;">
                        <p>SuRe Newsletter • Reliable Insights Delivered Weekly</p>
                        <p>Questions? Reply to this email and we'll get back to you!</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach both versions
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        
        return {
            "success": True,
            "message": f"Welcome email sent to {subscriber_email}"
        }
    
    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "error": "Email authentication failed. Check your credentials in .env"
        }
    except smtplib.SMTPException as e:
        return {
            "success": False,
            "error": f"SMTP error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to send email: {str(e)}"
        }

def send_newsletter(subscriber_emails: list, issue_title: str, issue_content: str) -> Dict:
    """Send newsletter to multiple subscribers"""
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return {
            "success": False,
            "error": "Email credentials not configured"
        }
    
    failed_count = 0
    success_count = 0
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            for email in subscriber_emails:
                try:
                    message = MIMEMultipart("alternative")
                    message["Subject"] = f"SuRe: {issue_title}"
                    message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
                    message["To"] = email
                    
                    # Simple HTML email
                    html = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                                <h1 style="color: #1E3A8A; text-align: center;">{issue_title}</h1>
                                <hr style="border: none; border-top: 2px solid #E2E8F0;">
                                <div style="color: #475569; line-height: 1.8;">
                                    {issue_content}
                                </div>
                                <hr style="border: none; border-top: 2px solid #E2E8F0; margin-top: 40px;">
                                <p style="text-align: center; color: #94A3B8; font-size: 12px;">
                                    SuRe Newsletter • Reliable Insights Delivered Weekly
                                </p>
                            </div>
                        </body>
                    </html>
                    """
                    
                    part = MIMEText(html, "html")
                    message.attach(part)
                    server.send_message(message)
                    success_count += 1
                except:
                    failed_count += 1
        
        return {
            "success": True,
            "sent": success_count,
            "failed": failed_count,
            "message": f"Newsletter sent to {success_count} subscribers"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to send newsletter: {str(e)}"
        }
