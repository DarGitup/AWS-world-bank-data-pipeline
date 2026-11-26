
import logging

from .api_client import WorldBankAPIClient

logger = logging.getLogger(__name__)


class WorldBankExtractor:
    def __init__(self):
        self.api_client = WorldBankAPIClient()

    def extract_all(self) -> dict:
        all_records = []
        page = 1
        total_pages = None
        total_records = None

        while total_pages is None or page <= total_pages:
            response = self.api_client.get_page(page)

            metadata = response["metadata"]
            records = response["records"]

            if total_pages is None:
                total_pages = int(metadata["pages"])
                total_records = int(metadata["total"])

                logger.info(
                    "Extraction started. Total pages: %s, Total records: %s",
                    total_pages,
                    total_records
                )

            all_records.extend(records)

            logger.info(
                "Page %s/%s completed. Records collected: %s",
                page,
                total_pages,
                len(all_records)
            )

            page += 1

        logger.info(
            "Extraction completed. Total records collected: %s",
            len(all_records)
        )

        return {
            "metadata": {
                "total_pages": total_pages,
                "total_records": total_records,
                "records_extracted": len(all_records)
            },
            "records": all_records
        }
