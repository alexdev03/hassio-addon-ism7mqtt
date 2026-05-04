# Pin immagine upstream: imposta ISM7MQTT_TAG in build.yaml (v0.0.19, master, …)
# BUILD_FROM viene scelto da build.yaml per architettura (HA Supervisor).
ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
ARG ISM7MQTT_TAG=v0.0.19
FROM zivillian/ism7mqtt:${ISM7MQTT_TAG} AS ism

FROM $BUILD_FROM

COPY run.sh /
RUN \
    apk add \
        icu-libs \
        moreutils \
        mosquitto-clients \
    && chmod a+x /run.sh

COPY --from=ism /app /app/

CMD [ "/run.sh" ]
