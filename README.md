# hassio-addon-ism7mqtt — pinned only

This repository contains **one** Home Assistant add-on: **Ism7MQTT (pinned image)**. It does **not** duplicate the stable or experimental add-ons from upstream, so you can add both this repo and [b3nn0/hassio-addon-ism7mqtt](https://github.com/b3nn0/hassio-addon-ism7mqtt) in the Add-on Store without seeing duplicate *Ism7MQTT* / *Ism7MQTT Experimental* entries from here.

## What this add-on does

**Ism7MQTT (pinned image)** uses a fixed Docker tag for `zivillian/ism7mqtt` (`build.yaml` → `ISM7MQTT_TAG`, default `v0.0.19`) instead of the moving `master` image. Use it if the official experimental add-on leaves some sensors stuck ([zivillian/ism7mqtt#205](https://github.com/zivillian/ism7mqtt/issues/205)). After changing the tag in `ism7mqtt-pinned/build.yaml`, **Rebuild** the add-on in Supervisor.

Do not run two add-ons against the same ISM7 (only one TCP session).

Fork: **https://github.com/alexdev03/hassio-addon-ism7mqtt** · Upstream community repo: **https://github.com/b3nn0/hassio-addon-ism7mqtt** · Core: **https://github.com/zivillian/ism7mqtt**

## Install (with upstream for other variants)

1. Settings → **Add-ons** → install **Mosquitto broker** (if needed) and start it.
2. Settings → **Devices & services** → add **MQTT** (use the local broker when asked).
3. Add-on Store → **Repositories**: add  
   - `https://github.com/b3nn0/hassio-addon-ism7mqtt` — for **Ism7MQTT** (stable) or **Ism7MQTT Experimental** if you want them  
   - `https://github.com/alexdev03/hassio-addon-ism7mqtt` — for **Ism7MQTT (pinned image)** only
4. Install **Ism7MQTT (pinned image)** from this repo; configure IP, password, device name like the upstream add-ons.
5. If something fails, check the add-on **Log** tab.

## Multiple ISM7 devices

Same pattern as upstream: use **additional ISM7 devices** in the add-on options. Details: [b3nn0 add-on README](https://github.com/b3nn0/hassio-addon-ism7mqtt/blob/main/README.md) (multi-instance section).

## Too many parameters / unstable ISM7

The ISM7 can be overwhelmed if you query hundreds of parameters. Mitigations (from upstream): reduce Wolf portal load, prefer Ethernet, trim `ism7-parameters-*.json`. See [b3nn0 README — “Important, if some entities are unavailable”](https://github.com/b3nn0/hassio-addon-ism7mqtt/blob/main/README.md).
