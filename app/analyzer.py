import logging
from typing import Dict, Any
from app.storage import storage
from app.utils import is_scanned_pdf

logger = logging.getLogger("analyzer")

class DocumentAnalyzer:
    @staticmethod
    def analyze(file_id: str) -> Dict[str, Any]:
        """
        Analyze the PDF to determine the best conversion strategy.
        Checks for text layer to ensure high-fidelity reflow is possible.
        """
        path = storage.get_path(file_id, "pdf", bucket="input")
        
        # Check if it's a scanned PDF (no text layer)
        scanned = is_scanned_pdf(path)
        
        analysis = {
            "has_text": not scanned,
            "needs_ocr": scanned,
            "complexity": "standard" if not scanned else "scanned",
            "strategy": "high_fidelity_reflow"  # Default for now
        }
        
        if scanned:
            logger.warning(f"File {file_id} appears to be scanned. OCR might be needed.")
        
        logger.info(f"Analysis complete for {file_id}: {analysis}")
        return analysis
