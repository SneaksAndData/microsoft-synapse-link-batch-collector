FROM python:3.11.9-slim-bookworm AS build-stage

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
 && apt-get --assume-yes upgrade \
 && apt-get --no-install-recommends --assume-yes install ca-certificates libgomp1 build-essential libssl-dev libffi-dev git \
 && mkdir -p /app/microsoft_synapse_batch_collector

WORKDIR /app/microsoft_synapse_batch_collector

COPY batchcollector/microsoft_synapse_batch_collector /app/microsoft_synapse_batch_collector
COPY .container/requirements.txt /tmp

RUN python3 -m venv .venv \
    && source .venv/bin/activate \
    && MAKEFLAGS="-j$(nproc)" pip3 install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

# Deploy the application binary into a lean image
FROM gcr.io/distroless/python3-debian12 AS build-release-stage

ENV PYTHONPATH=/app:/app/microsoft_synapse_batch_collector/.venv/lib/python3.11/site-packages
WORKDIR /app/microsoft_synapse_batch_collector

COPY --from=build-stage /app /app

USER nonroot:nonroot
