"""
 Cleanup.
"""
import os

from adapta.logs import LoggerInterface
from adapta.metrics import MetricsProvider
from adapta.storage.blob.azure_storage_client import AzureStorageClient
from adapta.storage.models import AdlsGen2Path
from adapta.utils.concurrent_task_runner import Executable, ConcurrentTaskRunner
from azure.storage.filedatalake import DataLakeServiceClient

from microsoft_synapse_batch_collector.models.uploaded_batch import UploadedBatch


def remove_batch(
    batch: UploadedBatch, client: AzureStorageClient, dry_run: bool, logger: LoggerInterface, metrics: MetricsProvider
) -> None:
    """
     Deletes all blobs that are part of the provided batch.

    :param batch: UploadedBatch
    :param client: AzureStorageClient
    :param dry_run: Delete or just print blobs to be removed
    :param logger: LoggerInterface
    :param metrics: MetricsProvider
    :return:
    """

    def _delete_blob(blob: AdlsGen2Path) -> bool:
        if not dry_run:
            logger.info("Deleting blob: {blob}", blob=blob.path)
            client.delete_leased_blob(blob)
            return True

        logger.info("Blob: {blob} qualifies for deletion. Skipping due to dry_run set to True", blob=blob.path)
        return False

    logger.info("Removing archived Synapse batch {batch}", batch=batch.source_path.path)
    metrics.gauge(
        metric_name="batch.total_blobs",
        metric_value=len(batch.blobs) - 1,
        tags={
            "batch": batch.source_path.path.split("/")[0],
        },
    )
    blob_delete_tasks = [
        Executable(
            func=_delete_blob,
            args=[
                blob_to_delete,
            ],
            alias=blob_to_delete.path,
        )
        for blob_to_delete in batch.blobs
    ]
    _ = ConcurrentTaskRunner(blob_delete_tasks, int(os.getenv("PROCESSING_THREADS", "128")), False).eager()

    # delete now-empty prefix - in case HNS is enabled, it will be retained as empty folder
    # HNS API is not supported in adapta - thus hacking it together here for now
    if os.getenv("HNS_ENABLED", "0") == "1" and not dry_run:
        DataLakeServiceClient(
            f"https://{batch.source_path.account}.dfs.core.windows.net",
            credential=os.getenv(f"PROTEUS__{batch.source_path.account.upper()}_AZURE_STORAGE_ACCOUNT_KEY"),
        ).get_directory_client(
            os.getenv("SYNAPSE_STORAGE_CONTAINER_NAME"), batch.source_path.path.rstrip("/")
        ).delete_directory()
