
import logging

from src.common.logger import setup_logger
from src.ingestion.extractor import WorldBankExtractor
from src.ingestion.s3_writer import S3Writer


def lambda_handler(event, context):
    setup_logger()
    logger = logging.getLogger(__name__)

    try:
        logger.info("World Bank ingestion pipeline started")

        # Step 1: Extract all API records
        extractor = WorldBankExtractor()
        extracted_data = extractor.extract_all()

        logger.info(
            "Extraction completed: %s records",
            extracted_data["metadata"]["records_extracted"]
        )

        # Step 2: Upload raw data to S3
        s3_writer = S3Writer()
        s3_key = s3_writer.upload_json(extracted_data)

        logger.info("World Bank ingestion pipeline completed")

        return {
            "statusCode": 200,
            "body": {
                "message": "Ingestion completed successfully",
                "records_extracted": extracted_data["metadata"]["records_extracted"],
                "s3_bucket": s3_writer.bucket,
                "s3_key": s3_key
            }
        }

    except Exception:
        logger.exception("World Bank ingestion pipeline failed")
        raise

if __name__ == "__main__":
    lambda_handler({}, None)