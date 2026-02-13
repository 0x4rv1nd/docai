import os
import subprocess
import logging
from pdf2docx import Converter
from app.storage import storage

logger = logging.getLogger("converter")

class ConversionStrategy:
    @staticmethod
    def high_fidelity_reflow(file_id: str) -> str:
        """
        Standard high-fidelity path: PDF -> DOCX -> PDF
        Ensures layout preservation and text editability.
        """
        pdf_path = storage.get_path(file_id, "pdf", bucket="input")
        docx_path = storage.get_path(file_id, "docx", bucket="input")
        
        # 1. PDF to DOCX
        try:
            cv = Converter(pdf_path)
            cv.convert(docx_path)
            cv.close()
        except Exception as e:
            logger.error(f"pdf2docx failed: {e}")
            raise

        # 2. DOCX to PDF (via LibreOffice)
        output_dir = os.path.dirname(storage.get_path(file_id, "pdf", bucket="output"))
        try:
            result = subprocess.run(
                [
                    "soffice", "--headless", "--convert-to", "pdf",
                    docx_path, "--outdir", output_dir
                ],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode != 0:
                raise Exception(f"LibreOffice error: {result.stderr}")
        except Exception as e:
            logger.error(f"LibreOffice failed: {e}")
            raise
        finally:
            # Cleanup docx
            storage.delete(file_id, "docx", bucket="input")
            
        return storage.get_path(file_id, "pdf", bucket="output")
