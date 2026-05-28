# WolfLink 300.x: binary sid in login XML — sidfix stage patches ism7mqtt.dll
ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
ARG ISM7MQTT_TAG=v0.0.19

FROM mcr.microsoft.com/dotnet/sdk:10.0 AS sidfix
ARG ISM7MQTT_TAG
RUN apt-get update && apt-get install -y --no-install-recommends git python3 \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch "${ISM7MQTT_TAG}" https://github.com/zivillian/ism7mqtt.git /src
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
