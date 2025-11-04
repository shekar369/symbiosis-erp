import re
from datetime import date


class Validators:
    @staticmethod
    def validate_employee_code(code: str) -> bool:
        """
        Validate employee code format
        """
        # Example: EMP001, EMP002, etc.
        pattern = r'^EMP\d{3,}$'
        return bool(re.match(pattern, code))

    @staticmethod
    def validate_pan(pan: str) -> bool:
        """
        Validate Indian PAN card format
        """
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
        return bool(re.match(pattern, pan))

    @staticmethod
    def validate_aadhar(aadhar: str) -> bool:
        """
        Validate Indian Aadhar card format
        """
        pattern = r'^\d{12}$'
        return bool(re.match(pattern, aadhar))

    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> bool:
        """
        Validate date range
        """
        return end_date >= start_date

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format
        """
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))
