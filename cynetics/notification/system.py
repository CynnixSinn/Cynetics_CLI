import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import requests
import json

class NotificationSystem:
    """A simple notification system supporting email and webhook notifications."""
    
    def __init__(self):
        self.email_config = None
        self.webhook_urls = []
    
    def configure_email(self, smtp_server: str, smtp_port: int, username: str, password: str, sender_email: str):
        """Configure email notifications."""
        self.email_config = {
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "username": username,
            "password": password,
            "sender_email": sender_email
        }
    
    def add_webhook_url(self, url: str):
        """Add a webhook URL for notifications."""
        self.webhook_urls.append(url)
    
    def send_email_notification(self, recipients: List[str], subject: str, message: str) -> bool:
        """Send an email notification to recipients."""
        if not self.email_config:
            print("Email not configured")
            return False
            
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config["sender_email"]
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to server and send email
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["username"], self.email_config["password"])
            text = msg.as_string()
            server.sendmail(self.email_config["sender_email"], recipients, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def send_webhook_notification(self, message: str, data: Dict[str, Any] = None) -> List[bool]:
        """Send a webhook notification to all configured URLs."""
        if data is None:
            data = {}
            
        data["message"] = message
        data["timestamp"] = __import__('datetime').datetime.now().isoformat()
        
        results = []
        for url in self.webhook_urls:
            try:
                response = requests.post(url, json=data)
                results.append(response.status_code == 200)
            except Exception as e:
                print(f"Failed to send webhook to {url}: {e}")
                results.append(False)
                
        return results
    
    def send_notification(self, message: str, recipients: List[str] = None, 
                        data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a notification via all configured channels."""
        results = {
            "email": False,
            "webhooks": []
        }
        
        # Send email if configured and recipients provided
        if self.email_config and recipients:
            results["email"] = self.send_email_notification(recipients, "Cynetics CLI Notification", message)
        
        # Send webhooks if configured
        if self.webhook_urls:
            results["webhooks"] = self.send_webhook_notification(message, data)
            
        return results