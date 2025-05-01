# Microsoft Synapse Link Batch Collector
Little helper for when your Synapse storage account needs a thorough cleaning.

## Quickstart
Execute the following to remove all Synapse batches older than 7 days and copy their contents to s3 under `<prefix>/<table>/<batch_date>_<partition>.csv`:
```shell
docker run -rm -it ... 
```