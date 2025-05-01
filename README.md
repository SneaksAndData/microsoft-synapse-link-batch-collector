# Microsoft Synapse Link Batch Collector
Little helper for when your Synapse storage account needs a thorough cleaning.

## Quickstart
Execute the following to remove all Synapse batches older than 7 days and copy their contents to AWS S3 or S3-compatible object storage under `<prefix>/<table>/<batch_date>_<partition>.csv`:
```shell
docker run -rm -it ghcr.io/sneaksanddata/microsoft-synapse-link-batch-collector:v1.0.0 \
  -e ADAPTA__AZURE_STORAGE_BLOB_ENDPOINT=https://myaccount.blob.core.windows.net" \
  -e PROTEUS__MYACCOUNT_AZURE_STORAGE_ACCOUNT_KEY=... \
  -e S3_DESTINATION__ACCESS_KEY=... \
  -e S3_DESTINATION__ACCESS_KEY_ID=... \
  -e S3_DESTINATION__REGION=... \
  -e S3_DESTINATION__ENDPOINT=http://s3.<region>.amazonaws.com \
  --upload-to-bucket my-bucket \
  --upload-to-prefix my-dynamics-env \
  --batch-older-than-days 7 \
  --synapse-source-path 'abfss://container@account.dfs.core.windows.net' \
  --remove-processed-batches
```
