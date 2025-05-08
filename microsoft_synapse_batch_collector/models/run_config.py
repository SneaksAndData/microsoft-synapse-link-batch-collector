"""
 Models for runtime config.
"""
import argparse
import os
from dataclasses import dataclass

from adapta.storage.models import AdlsGen2Path


@dataclass
class RunConfig:
    """
    Run configuration
    """

    upload_bucket_name: str
    prefix: str
    age_threshold: int
    synapse_source_path: AdlsGen2Path
    delete_processed: bool

    @classmethod
    def from_input_args(cls, input_args: argparse.Namespace) -> "RunConfig":
        """
         Parse input arguments into a RunConfig object.
        :param input_args:
        :return:
        """
        return RunConfig(
            upload_bucket_name=input_args.upload_to_bucket,
            prefix=input_args.upload_to_prefix,
            age_threshold=input_args.batch_older_than_days,
            synapse_source_path=AdlsGen2Path.from_hdfs_path(input_args.synapse_source_path)
            if input_args.synapse_source_path
            else AdlsGen2Path.from_hdfs_path(
                f"{os.environ['SYNAPSE_STORAGE_CONTAINER_NAME']}@{os.environ['SYNAPSE_STORAGE_ACCOUNT_NAME']}.dfs.core.windows.net"
            ),
            delete_processed=input_args.remove_processed_batches,
        )
