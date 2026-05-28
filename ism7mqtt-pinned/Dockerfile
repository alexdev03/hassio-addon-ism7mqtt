# WolfLink 300.x sidfix + zivillian/ism7mqtt PR #211 (race condition / bundle ID sync)
ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
ARG ISM7MQTT_TAG=master
ARG ISM7MQTT_MERGE_PR=211
ARG ISM7MQTT_CLONE_DEPTH=50

FROM mcr.microsoft.com/dotnet/sdk:10.0 AS sidfix
ARG ISM7MQTT_TAG
ARG ISM7MQTT_MERGE_PR
ARG ISM7MQTT_CLONE_DEPTH
RUN apt-get update && apt-get install -y --no-install-recommends git python3 \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth "${ISM7MQTT_CLONE_DEPTH}" --branch "${ISM7MQTT_TAG}" \
        https://github.com/zivillian/ism7mqtt.git /src \
    && cd /src \
    && git fetch origin "pull/${ISM7MQTT_MERGE_PR}/head:pr-merge" \
    && git config user.email "docker@build" \
    && git config user.name "Docker Build" \
    && git merge --no-edit pr-merge
COPY sidfix/patch_ism7.py /tmp/patch_ism7.py
RUN python3 /tmp/patch_ism7.py \
    && dotnet publish /src/src/ism7mqtt/ism7mqtt.csproj -c Release -o /out

FROM zivillian/ism7mqtt:${ISM7MQTT_TAG} AS ism
COPY --from=sidfix /out/ism7mqtt.dll /app/ism7mqtt.dll

FROM ${BUILD_FROM}

COPY run.sh /
RUN \
    apk add \
        icu-libs \
        moreutils \
        mosquitto-clients \
    && chmod a+x /run.sh

COPY --from=ism /app /app/

CMD [ "/run.sh" ]
