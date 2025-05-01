#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from azure.storage.blob import BlobServiceClient, BlobLeaseClient
from datetime import datetime, timedelta

import random


CONTENT = """10bff458-d47a-4924-804b-31c0a83108e6,"1/1/2020 0:00:00 PM","1/1/2020 0:00:00 PM",0,1111000000,1111000010,"F1234567",1,,"2020-01-01T00:15:00.0000000Z","acc1",111111110,"2020-01-01T00:15:00.0000000Z","acc1",0,"dat",1,1111000001,2111000001,1111000001,21111,2111000001,"2020-01-01T00:15:00.0000000+00:00","2020-01-01T00:15:00.0000000Z",
2b4bc74e-2132-4d8e-8572-48ce4260f182,"1/1/2020 0:00:01 PM","1/1/2020 0:00:01 PM",0,1111000001,1111000011,"F1234568",1,,"2020-01-01T00:16:00.0000000Z","acc2",111111111,"2020-01-01T00:16:00.0000000Z","acc2",0,"dat",1,1111000002,2111000002,1111000001,21111,2111000001,"2020-01-01T00:16:00.0000000+00:00","2020-01-01T00:16:00.0000000Z",
3ae2094d-cd17-42b4-891e-3b268e2b6713,"1/1/2020 0:00:01 PM","1/1/2020 0:00:01 PM",0,1111000002,1111000012,"F1234569",1,,"2020-01-01T00:17:00.0000000Z","acc2",111111112,"2020-01-01T00:17:00.0000000Z","acc2",0,"dat",1,1111000003,2111000003,1111000001,21111,2111000001,"2020-01-01T00:17:00.0000000+00:00","2020-01-01T00:17:00.0000000Z",
4633be9a-c485-4afa-8bb7-4ba380eaa206,"1/1/2020 0:00:01 PM","1/1/2020 0:00:01 PM",0,1111000003,1111000013,"F1234578",1,,"2020-01-01T00:18:00.0000000Z","acc1",111111113,"2020-01-01T00:18:00.0000000Z","acc1",0,"dat",1,1111000004,2111000004,1111000001,21111,2111000001,"2020-01-01T00:18:00.0000000+00:00","2020-01-01T00:18:00.0000000Z",
562c7b67-b8f8-4635-8cef-1c23591d5c4c,"1/1/2020 0:00:01 PM","1/1/2020 0:00:01 PM",0,1111000004,1111000014,"F1234511",1,,"2020-01-01T00:19:00.0000000Z","acc2",111111114,"2020-01-01T00:19:00.0000000Z","acc2",0,"dat",1,1111000005,2111000005,1111000001,21111,2111000001,"2020-01-01T00:19:00.0000000+00:00","2020-01-01T00:19:00.0000000Z",
562c7b67-b8f8-4635-8cef-1c23591d5c4c,"1/1/2020 0:00:01 PM","1/1/2020 0:00:01 PM",0,1111000004,1111000014,"F1234511",1,,"2020-01-01T00:19:00.0000000Z","acc2",111111114,"2020-01-01T00:19:00.0000000Z","acc2",0,"dat",1,1111000005,2111000005,1111000001,21111,2111000001,"2020-01-01T00:19:00.0000000+00:00","2020-01-01T00:19:00.0000000Z",
"""

MODEL_JSON = """{
                  "name": "cdm",
                  "description": "cdm",
                  "version": "1.0",
                  "entities": [
                    {
                      "$type": "LocalEntity",
                      "name": "currency",
                      "description": "currency",
                      "annotations": [
                        {
                          "name": "Athena:PartitionGranularity",
                          "value": "Year"
                        },
                        {
                          "name": "Athena:InitialSyncState",
                          "value": "Completed"
                        },
                        {
                          "name": "Athena:InitialSyncDataCompletedTime",
                          "value": "1/1/2020 0:00:00 PM"
                        }
                      ],
                      "attributes": [
                        {
                          "name": "Id",
                          "dataType": "guid",
                          "maxLength": -1
                        },
                        {
                          "name": "SinkCreatedOn",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "SinkModifiedOn",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "iseuro",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "roundofftypeassetdep_jp",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "roundofftypeprice",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "roundofftypepurch",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "roundofftypesales",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "ltmroundofftypelineamount",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "sysdatastatecode",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "currencycode",
                          "dataType": "string",
                          "maxLength": 3,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 3
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "currencycodeiso",
                          "dataType": "string",
                          "maxLength": 3,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 3
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "roundingprecision",
                          "dataType": "decimal",
                          "maxLength": -1,
                          "cdm:traits": [
                            {
                              "traitReference": "is.dataFormat.numeric.shaped",
                              "arguments": [
                                {
                                  "name": "precision",
                                  "value": 38
                                },
                                {
                                  "name": "scale",
                                  "value": 6
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "roundoffassetdep_jp",
                          "dataType": "decimal",
                          "maxLength": -1,
                          "cdm:traits": [
                            {
                              "traitReference": "is.dataFormat.numeric.shaped",
                              "arguments": [
                                {
                                  "name": "precision",
                                  "value": 38
                                },
                                {
                                  "name": "scale",
                                  "value": 6
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "roundoffprice",
                          "dataType": "decimal",
                          "maxLength": -1,
                          "cdm:traits": [
                            {
                              "traitReference": "is.dataFormat.numeric.shaped",
                              "arguments": [
                                {
                                  "name": "precision",
                                  "value": 38
                                },
                                {
                                  "name": "scale",
                                  "value": 6
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "roundoffpurch",
                          "dataType": "decimal",
                          "maxLength": -1,
                          "cdm:traits": [
                            {
                              "traitReference": "is.dataFormat.numeric.shaped",
                              "arguments": [
                                {
                                  "name": "precision",
                                  "value": 38
                                },
                                {
                                  "name": "scale",
                                  "value": 6
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "roundoffsales",
                          "dataType": "decimal",
                          "maxLength": -1,
                          "cdm:traits": [
                            {
                              "traitReference": "is.dataFormat.numeric.shaped",
                              "arguments": [
                                {
                                  "name": "precision",
                                  "value": 38
                                },
                                {
                                  "name": "scale",
                                  "value": 6
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "symbol",
                          "dataType": "string",
                          "maxLength": 5,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 5
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "txt",
                          "dataType": "string",
                          "maxLength": 120,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 120
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "exchratemaxvariationpercent_mx",
                          "dataType": "decimal",
                          "maxLength": -1,
                          "cdm:traits": [
                            {
                              "traitReference": "is.dataFormat.numeric.shaped",
                              "arguments": [
                                {
                                  "name": "precision",
                                  "value": 38
                                },
                                {
                                  "name": "scale",
                                  "value": 6
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "decimalscount_mx",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "ltmroundofflineamount",
                          "dataType": "decimal",
                          "maxLength": -1,
                          "cdm:traits": [
                            {
                              "traitReference": "is.dataFormat.numeric.shaped",
                              "arguments": [
                                {
                                  "name": "precision",
                                  "value": 38
                                },
                                {
                                  "name": "scale",
                                  "value": 6
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "modifieddatetime",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "modifiedby",
                          "dataType": "string",
                          "maxLength": 20,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 20
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "modifiedtransactionid",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "createddatetime",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "createdby",
                          "dataType": "string",
                          "maxLength": 20,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 20
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "createdtransactionid",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "dataareaid",
                          "dataType": "string",
                          "maxLength": 4,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 4
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "recversion",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "partition",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "sysrowversion",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "recid",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "tableid",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "versionnumber",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "createdon",
                          "dataType": "dateTimeOffset",
                          "maxLength": -1
                        },
                        {
                          "name": "modifiedon",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "IsDelete",
                          "dataType": "boolean",
                          "maxLength": -1
                        }
                      ],
                      "partitions": []
                    },
                    {
                      "$type": "LocalEntity",
                      "name": "synapsetable",
                      "description": "synapsetable",
                      "annotations": [
                        {
                          "name": "Athena:PartitionGranularity",
                          "value": "Year"
                        },
                        {
                          "name": "Athena:InitialSyncState",
                          "value": "Completed"
                        },
                        {
                          "name": "Athena:InitialSyncDataCompletedTime",
                          "value": "1/1/2020 0:00:00 PM"
                        }
                      ],
                      "attributes": [
                        {
                          "name": "Id",
                          "dataType": "guid",
                          "maxLength": -1
                        },
                        {
                          "name": "SinkCreatedOn",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "SinkModifiedOn",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "sysdatastatecode",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "dimensionattributevalue",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "dimensionattributevaluegroup",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "displayvalue",
                          "dataType": "string",
                          "maxLength": 30,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 30
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "ordinal",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "backingrecorddataareaid",
                          "dataType": "string",
                          "maxLength": 4,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 4
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "modifieddatetime",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "modifiedby",
                          "dataType": "string",
                          "maxLength": 20,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 20
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "modifiedtransactionid",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "createddatetime",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "createdby",
                          "dataType": "string",
                          "maxLength": 20,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 20
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "createdtransactionid",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "dataareaid",
                          "dataType": "string",
                          "maxLength": 4,
                          "cdm:traits": [
                            {
                              "traitReference": "is.constrained",
                              "arguments": [
                                {
                                  "name": "maximumLength",
                                  "value": 4
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "name": "recversion",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "partition",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "sysrowversion",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "recid",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "tableid",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "versionnumber",
                          "dataType": "int64",
                          "maxLength": -1
                        },
                        {
                          "name": "createdon",
                          "dataType": "dateTimeOffset",
                          "maxLength": -1
                        },
                        {
                          "name": "modifiedon",
                          "dataType": "dateTime",
                          "maxLength": -1
                        },
                        {
                          "name": "IsDelete",
                          "dataType": "boolean",
                          "maxLength": -1
                        }
                      ],
                      "partitions": []
                    }
                  ]
                }"""

AZURITE_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10001/devstoreaccount1"
ARCHIVE_CONTAINER = "synapse-archiving-test"
# Get the current date and time
now = datetime.utcnow()

# for archiving tests, subtract 1 week + 2 days
archive_start_time = now - timedelta(hours=216)

ARCHIVE_FOLDERS = [(archive_start_time + timedelta(hours=i)).strftime("%Y-%m-%dT%H.%M.%SZ") for i in range(216)]
LATEST_ARCHIVE = max(ARCHIVE_FOLDERS)


def upload_blob_file(blob_service_client: BlobServiceClient, container_name: str, blob_name: str, content: str):
    blob_service_client.get_container_client(container=container_name).upload_blob(
        name=blob_name, data=content.encode("utf-8"), overwrite=True
    )


def lease_blob_file(blob_service_client: BlobServiceClient, container_name: str, blob_name: str):
    BlobLeaseClient(blob_service_client.get_blob_client(container=container_name, blob=blob_name)).acquire()


def create_archive_container():
    # Create a container for Azurite for the first run
    blob_service_client = BlobServiceClient.from_connection_string(AZURITE_CONNECTION_STRING)
    try:
        blob_service_client.create_container(ARCHIVE_CONTAINER)
    except Exception as e:
        print(e)


def create_archive_blobs(model_json, content, folders):
    blob_service_client = BlobServiceClient.from_connection_string(AZURITE_CONNECTION_STRING)
    for folder in folders:
        upload_blob_file(blob_service_client, ARCHIVE_CONTAINER, f"{folder}/model.json", model_json)
        upload_blob_file(blob_service_client, ARCHIVE_CONTAINER, f"{folder}/synapsetable/2020.csv", content)
        upload_blob_file(blob_service_client, ARCHIVE_CONTAINER, f"{folder}/synapsetable/2021.csv", content)
        upload_blob_file(blob_service_client, ARCHIVE_CONTAINER, f"{folder}/synapsetable/2022.csv", content)
        upload_blob_file(blob_service_client, ARCHIVE_CONTAINER, f"{folder}/synapsetable_other/2020.csv", content)
        if random.random() > 0.2:
            lease_blob_file(blob_service_client, ARCHIVE_CONTAINER, f"{folder}/synapsetable/2020.csv")
    # upload changelog
    upload_blob_file(blob_service_client, ARCHIVE_CONTAINER, f"Changelog/changelog.info", LATEST_ARCHIVE)


create_archive_container()
create_archive_blobs(MODEL_JSON, CONTENT, ARCHIVE_FOLDERS)

blob_service_client = BlobServiceClient.from_connection_string(AZURITE_CONNECTION_STRING)
upload_blob_file(blob_service_client, ARCHIVE_CONTAINER, "model.json", MODEL_JSON)
