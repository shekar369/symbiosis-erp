from typing import List, Dict, Tuple, Callable, Any
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import os
import tempfile
import logging

from app.utils.excel_parser import ExcelParser

logger = logging.getLogger(__name__)


class UploadService:
    """Centralized service for handling file uploads with validation and processing"""

    ALLOWED_EXTENSIONS = ('.xlsx', '.xls')
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """Validate uploaded file type and size"""
        if not file.filename.endswith(UploadService.ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only Excel files {UploadService.ALLOWED_EXTENSIONS} are supported"
            )

        # TODO: Add file size validation when implementing max size check

    @staticmethod
    async def save_temp_file(file: UploadFile) -> str:
        """Save uploaded file to temporary location"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                return tmp_file.name
        except Exception as e:
            logger.error(f"Failed to save temporary file: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process uploaded file"
            )

    @staticmethod
    def cleanup_temp_file(file_path: str) -> None:
        """Remove temporary file safely"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file {file_path}: {str(e)}")

    @staticmethod
    def process_upload(
        db: Session,
        file_path: str,
        parser_func: Callable,
        record_processor: Callable[[Dict, Session], None],
        max_errors: int = 100
    ) -> Dict[str, Any]:
        """
        Generic upload processing logic

        Args:
            db: Database session
            file_path: Path to temporary file
            parser_func: Function to parse Excel file (returns valid_records, errors)
            record_processor: Function to process each valid record
            max_errors: Maximum errors to return in response

        Returns:
            Dict with upload summary and errors
        """
        try:
            valid_records, validation_errors = parser_func(file_path)

            uploaded_count = 0
            failed_count = 0
            errors_list = [error.to_dict() for error in validation_errors]

            for record in valid_records:
                try:
                    record_processor(record, db)
                    uploaded_count += 1
                except HTTPException as e:
                    # Re-raise HTTP exceptions
                    errors_list.append({
                        "row": "N/A",
                        "column": "general",
                        "value": record.get('employee_code', 'Unknown'),
                        "error": e.detail
                    })
                    failed_count += 1
                except Exception as e:
                    logger.error(f"Error processing record: {str(e)}", exc_info=True)
                    errors_list.append({
                        "row": "N/A",
                        "column": "general",
                        "value": str(record.get('employee_code', 'Unknown')),
                        "error": str(e)
                    })
                    failed_count += 1

            # Commit only if we have successful uploads
            if uploaded_count > 0:
                db.commit()

            return {
                "success": True,
                "message": f"Upload complete. {uploaded_count} records uploaded, {failed_count} failed.",
                "summary": {
                    "total_rows": len(valid_records) + len(validation_errors),
                    "uploaded": uploaded_count,
                    "failed": failed_count,
                    "validation_errors": len(validation_errors)
                },
                "errors": errors_list[:max_errors]
            }

        except Exception as e:
            logger.error(f"Upload processing failed: {str(e)}", exc_info=True)
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing file: {str(e)}"
            )
