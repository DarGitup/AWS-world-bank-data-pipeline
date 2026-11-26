
import logging
import time

import requests

from ..common.config import config

logger = logging.getLogger(__name__)


class WorldBankAPIClient:
    def __init__(self):
        self.base_url = config.api_url
        self.timeout = config.api_timeout
        self.max_retries = 3

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "world-bank-data-pipeline/1.0"
        })

    def get_page(self, page: int) -> dict:
        params = {
            "format": "json",
            "page": page,
            "per_page": config.page_size
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info("Requesting World Bank API page %s", page)

                response = self.session.get(
                    self.base_url,
                    params=params,
                    timeout=self.timeout
                )

                response.raise_for_status()

                data = response.json()

                if not isinstance(data, list) or len(data) != 2:
                    raise ValueError(
                        f"Unexpected API response structure for page {page}"
                    )

                metadata, records = data

                if not isinstance(metadata, dict) or not isinstance(records, list):
                    raise ValueError(
                        f"Invalid metadata or records for page {page}"
                    )

                logger.info(
                    "Successfully fetched page %s: %s records",
                    page,
                    len(records)
                )

                return {
                    "metadata": metadata,
                    "records": records
                }

            except (requests.RequestException, ValueError):
                logger.exception(
                    "Failed to fetch page %s (attempt %s/%s)",
                    page,
                    attempt,
                    self.max_retries
                )

                if attempt == self.max_retries:
                    raise

                time.sleep(2 ** (attempt - 1))

        raise RuntimeError(f"Unable to fetch page {page}")
