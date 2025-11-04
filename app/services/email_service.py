import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional, Dict, Any
from io import BytesIO
import os
from datetime import datetime


class EmailService:
    """Email service for sending payslips and notifications"""

    def __init__(
        self,
        smtp_host: str = None,
        smtp_port: int = None,
        smtp_username: str = None,
        smtp_password: str = None,
        use_tls: bool = True
    ):
        """
        Initialize email service with SMTP configuration

        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            smtp_username: SMTP username
            smtp_password: SMTP password
            use_tls: Use TLS encryption
        """
        # Get config from environment or parameters
        self.smtp_host = smtp_host or os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = smtp_username or os.getenv('SMTP_USERNAME', '')
        self.smtp_password = smtp_password or os.getenv('SMTP_PASSWORD', '')
        self.use_tls = use_tls
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)
        self.from_name = os.getenv('FROM_NAME', 'HR Payroll System')

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_html: str,
        body_text: str = None,
        attachments: List[Dict[str, Any]] = None
    ) -> bool:
        """
        Send email with optional attachments

        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML email body
            body_text: Plain text email body (fallback)
            attachments: List of dicts with 'filename' and 'content' (BytesIO)

        Returns:
            bool: True if sent successfully
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

            # Add plain text version
            if body_text:
                part_text = MIMEText(body_text, 'plain')
                msg.attach(part_text)

            # Add HTML version
            part_html = MIMEText(body_html, 'html')
            msg.attach(part_html)

            # Add attachments
            if attachments:
                for attachment in attachments:
                    filename = attachment.get('filename', 'attachment')
                    content = attachment.get('content')  # BytesIO object

                    if content:
                        content.seek(0)  # Reset to beginning
                        part = MIMEApplication(content.read(), Name=filename)
                        part['Content-Disposition'] = f'attachment; filename="{filename}"'
                        msg.attach(part)

            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()

                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)

                server.send_message(msg)

            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_payslip_email(
        self,
        employee_email: str,
        employee_name: str,
        month: int,
        year: int,
        payslip_pdf: BytesIO,
        company_name: str = "Company"
    ) -> bool:
        """
        Send payslip email to employee

        Args:
            employee_email: Employee's email address
            employee_name: Employee's full name
            month: Month number
            year: Year
            payslip_pdf: PDF file as BytesIO
            company_name: Company name

        Returns:
            bool: True if sent successfully
        """
        subject = f"Payslip for {month:02d}/{year} - {company_name}"

        # HTML email body
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1e40af; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                .button {{ display: inline-block; padding: 10px 20px; background-color: #1e40af;
                          color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{company_name}</h1>
                    <h2>Salary Slip</h2>
                </div>
                <div class="content">
                    <p>Dear {employee_name},</p>

                    <p>Please find attached your salary slip for <strong>{month:02d}/{year}</strong>.</p>

                    <p>Your payslip is attached as a PDF file. Please download and save it for your records.</p>

                    <p><strong>Important:</strong></p>
                    <ul>
                        <li>Keep this payslip for your tax records</li>
                        <li>Verify all details and report any discrepancies to HR</li>
                        <li>This is a confidential document</li>
                    </ul>

                    <p>If you have any questions regarding your salary, please contact the HR department.</p>

                    <p>Best regards,<br>
                    <strong>HR Department</strong><br>
                    {company_name}</p>
                </div>
                <div class="footer">
                    <p>This is an automated email. Please do not reply to this message.</p>
                    <p>&copy; {year} {company_name}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Plain text version
        body_text = f"""
        Dear {employee_name},

        Please find attached your salary slip for {month:02d}/{year}.

        Your payslip is attached as a PDF file. Please download and save it for your records.

        Important:
        - Keep this payslip for your tax records
        - Verify all details and report any discrepancies to HR
        - This is a confidential document

        If you have any questions regarding your salary, please contact the HR department.

        Best regards,
        HR Department
        {company_name}

        ---
        This is an automated email. Please do not reply to this message.
        © {year} {company_name}. All rights reserved.
        """

        # Prepare attachment
        attachments = [{
            'filename': f'payslip_{month:02d}_{year}.pdf',
            'content': payslip_pdf
        }]

        return self.send_email(
            to_email=employee_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
            attachments=attachments
        )

    def send_bulk_payslips(
        self,
        payslip_data_list: List[Dict[str, Any]],
        company_name: str = "Company"
    ) -> Dict[str, Any]:
        """
        Send payslips to multiple employees

        Args:
            payslip_data_list: List of dicts with employee_email, employee_name,
                               month, year, payslip_pdf
            company_name: Company name

        Returns:
            dict: Summary with successful and failed counts
        """
        successful = 0
        failed = 0
        failed_emails = []

        for payslip_data in payslip_data_list:
            try:
                result = self.send_payslip_email(
                    employee_email=payslip_data['employee_email'],
                    employee_name=payslip_data['employee_name'],
                    month=payslip_data['month'],
                    year=payslip_data['year'],
                    payslip_pdf=payslip_data['payslip_pdf'],
                    company_name=company_name
                )

                if result:
                    successful += 1
                else:
                    failed += 1
                    failed_emails.append(payslip_data['employee_email'])

            except Exception as e:
                failed += 1
                failed_emails.append(payslip_data['employee_email'])
                print(f"Error sending to {payslip_data.get('employee_email')}: {str(e)}")

        return {
            'total': len(payslip_data_list),
            'successful': successful,
            'failed': failed,
            'failed_emails': failed_emails
        }

    def send_notification(
        self,
        to_email: str,
        subject: str,
        message: str,
        notification_type: str = "info"
    ) -> bool:
        """
        Send simple notification email

        Args:
            to_email: Recipient email
            subject: Email subject
            message: Notification message
            notification_type: Type of notification (info, warning, success, error)

        Returns:
            bool: True if sent successfully
        """
        colors = {
            'info': '#1e40af',
            'warning': '#f59e0b',
            'success': '#10b981',
            'error': '#ef4444'
        }

        color = colors.get(notification_type, '#1e40af')

        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: {color}; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{subject}</h2>
                </div>
                <div class="content">
                    <p>{message}</p>
                </div>
            </div>
        </body>
        </html>
        """

        body_text = f"{subject}\n\n{message}"

        return self.send_email(
            to_email=to_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text
        )

    def test_connection(self) -> bool:
        """
        Test SMTP connection

        Returns:
            bool: True if connection successful
        """
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                if self.use_tls:
                    server.starttls()

                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)

                return True

        except Exception as e:
            print(f"SMTP connection test failed: {str(e)}")
            return False
