"""
 Archiving.
"""
import os
from datetime import datetime, timedelta
from typing import Iterator

from adapta.logs import LoggerInterface
from adapta.metrics import MetricsProvider
from adapta.storage.blob.azure_storage_client import AzureStorageClient
from adapta.storage.blob.s3_storage_client import S3StorageClient
from adapta.storage.models import AdlsGen2Path, S3Path, DataPath
from adapta.utils import operation_time
from adapta.utils.concurrent_task_runner import Executable, ConcurrentTaskRunner

from microsoft_synapse_batch_collector.models.uploaded_batch import UploadedBatch
from microsoft_synapse_batch_collector.processing.synapse import filter_batches


def _valid_blob(blob_name: str) -> bool:
    """
    Exclude blobs with Synapse metadata folders in path
    """
    for segment in ["OptionsetMetadata", "Microsoft.Athena.TrickleFeedService"]:
        if segment in blob_name:
            return False

    if blob_name.endswith(".csv"):
        return True

    return False


def transform_path(azure_path: AdlsGen2Path, bucket: str, prefix: str) -> S3Path:
    """
    Transforms Synapse Link location into S3 prefix
    """
    segments = azure_path.path.split("/")
    return S3Path(
        bucket=bucket,
        path="/".join([prefix, segments[1], f"{segments[0].replace('.', '-')}_{segments[2]}"]),
    )


def upload_batches(
    source: AdlsGen2Path,
    bucket: str,
    prefix: str,
    threshold: int,
    logger: LoggerInterface,
    source_client: AzureStorageClient,
    target_client: S3StorageClient,
    metrics: MetricsProvider,
) -> Iterator[UploadedBatch]:
    """
    Process all files for the specified region, starting from dag_run_date
    """

    def _copy_blob(blob: DataPath) -> bool:
        with operation_time() as ot:
            local_dirs = "/".join(["/tmp"] + blob.path.split("/")[:-1])
            target_path = transform_path(blob, bucket, prefix)

            logger.info(
                "Copying {synapse_file} to {target_path}",
                synapse_file=blob.to_hdfs_path(),
                target_path=target_path.to_hdfs_path(),
            )
            os.makedirs(local_dirs, exist_ok=True)

            source_client.download_blobs(blob, "/tmp")
            target_client.upload_blob(f"/tmp/{blob.path}", target_path, doze_period_ms=0)
            os.remove(f"/tmp/{blob.path}")

            logger.info(
                "Successfully copied {synapse_file} to {target_path}",
                synapse_file=blob.to_hdfs_path(),
                target_path=target_path.to_hdfs_path(),
            )

        metrics.gauge("batch.copy_duration", ot.elapsed / 1e9, tags={"file": blob.path})
        return True

    logger.info(
        "Running with source: {source}, target: {bucket}/{prefix}",
        source=source.to_hdfs_path(),
        bucket=bucket,
        prefix=prefix,
    )
    start_from_batch = (datetime.utcnow() - timedelta(days=threshold)).strftime("%Y-%m-%dT%H.%M.%SZ")

    for synapse_prefix in filter_batches(
        storage_client=source_client,
        base_path=source,
        start_from=start_from_batch,
        logger=logger,
    ):
        logger.info(
            "Batch {batch_folder} is older than {threshold} days, archiving",
            batch_folder=synapse_prefix.to_hdfs_path(),
            threshold=threshold,
        )
        associated_blobs = list(source_client.list_blobs(blob_path=synapse_prefix))

        blob_copy_tasks = [
            Executable(
                func=_copy_blob,
                args=[
                    synapse_blob,
                ],
                alias=synapse_blob.path,
            )
            for synapse_blob in associated_blobs
            if _valid_blob(synapse_blob.path)
        ]
        _ = ConcurrentTaskRunner(blob_copy_tasks, int(os.getenv("PROCESSING_THREADS", "128")), False).eager()

        logger.info("Finished archiving batch {batch}", batch=synapse_prefix.path)

        yield UploadedBatch(
            source_path=synapse_prefix,
            blobs=associated_blobs,
        )
