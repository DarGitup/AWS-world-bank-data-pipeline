
import json
import logging
from datetime import datetime, timezone

import boto3

from src.common.config import config

logger = logging.getLogger(__name__)


class S3Writer:
    def __init__(self):
        if not config.s3_bucket:
            raise ValueError("S3_BUCKET is not configured in .env")

        self.bucket = config.s3_bucket
        self.prefix = config.s3_prefix

        self.s3_client = boto3.client(
            "s3",
            region_name=config.aws_region
        )

    def upload_json(self, data: dict) -> str:
        timestamp = datetime.now(timezone.utc)

        file_name = (
            f"population_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        )

        s3_key = f"{self.prefix}/{timestamp.strftime('%Y/%m/%d')}/{file_name}"

        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=s3_key,
            Body=json.dumps(data, ensure_ascii=False).encode("utf-8"),
            ContentType="application/json"
        )

        logger.info(
            "Successfully uploaded data to s3://%s/%s",
            self.bucket,
            s3_key
        )

        return s3_key
