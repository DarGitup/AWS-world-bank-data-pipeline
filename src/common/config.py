import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()


@dataclass(frozen=True)
class Config:
    # World Bank API configuration
    api_url: str = os.getenv(
        "WORLD_BANK_API_URL",
        "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"
    )

    page_size: int = int(os.getenv("API_PAGE_SIZE", "1000"))

    api_timeout: int = int(os.getenv("API_TIMEOUT", "30"))

    # AWS configuration
    s3_bucket: str = os.getenv("S3_BUCKET", "")

    s3_prefix: str = os.getenv(
        "S3_PREFIX",
        "raw/world_bank/population"
    )

    aws_region: str = os.getenv(
        "AWS_REGION",
        "ap-southeast-2"
    )


config = Config()