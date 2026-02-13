import logging
from app.analyzer import DocumentAnalyzer
from app.converter.strategy import ConversionStrategy
from app.storage import storage

logger = logging.getLogger("converter-main")

async def process_conversion(file_id: str):
    """
    Orchestrate the conversion process: analyze -> choose strategy -> execute.
    """
    try:
        # 1. Analyze
        analysis = DocumentAnalyzer.analyze(file_id)
        
        # 2. Convert based on strategy
        if analysis["strategy"] == "high_fidelity_reflow":
            ConversionStrategy.high_fidelity_reflow(file_id)
        else:
            # Fallback or other strategies
            ConversionStrategy.high_fidelity_reflow(file_id)
            
        logger.info(f"Conversion successful for {file_id}")
    except Exception as e:
        logger.error(f"Conversion failed for {file_id}: {str(e)}")
    finally:
        # Cleanup original input PDF
        storage.delete(file_id, "pdf", bucket="input")
