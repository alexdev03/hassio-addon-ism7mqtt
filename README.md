# hassio-addon-ism7mqtt — pinned only

This repository contains **one** Home Assistant add-on: **Ism7MQTT (pinned image)**. It does **not** duplicate the stable or experimental add-ons from upstream, so you can add both this repo and [b3nn0/hassio-addon-ism7mqtt](https://github.com/b3nn0/hassio-addon-ism7mqtt) in the Add-on Store without seeing duplicate *Ism7MQTT* / *Ism7MQTT Experimental* entries from here.

## WolfLink 300.x — sidfix (login XML `0x01`)

On **WOLFLink** firmware **300.x**, the login `sid` attribute can contain binary bytes; stock `ism7mqtt` crashes on every fresh login ([ism7mqtt#177](https://github.com/zivillian/ism7mqtt/issues/177)) — typical after a Home Assistant or add-on restart (restart loop).

This fork **builds a patched `ism7mqtt.dll`** during the Docker image build (`ism7mqtt-pinned/sidfix/patch_ism7.py`).

After `git pull`: **Supervisor → add-on → Rebuild** (5–15 min, needs internet). Disable any automation that restarts the add-on every hour until stable.

## What this add-on does

**Ism7MQTT (pinned image)** builds `zivillian/ism7mqtt` from a configurable base tag (`build.yaml` → `ISM7MQTT_TAG`, default `master`) and **merges upstream PR #211** at build time (`ISM7MQTT_MERGE_PR`) for the race-condition / bundle-ID fix ([zivillian/ism7mqtt#211](https://github.com/zivillian/ism7mqtt/pull/211), [issue #205](https://github.com/zivillian/ism7mqtt/issues/205)). A **sidfix** patch for WolfLink 300.x login XML is applied on top. After changing `ism7mqtt-pinned/build.yaml`, **Rebuild** the add-on in Supervisor (5–15 min, needs internet).

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

## Migrating from Experimental on this fork

If you previously used **Ism7MQTT Experimental** from an older commit of this repo: stop it, install **Ism7MQTT (pinned image)** from the same repository URL, copy the same options (IP, password, device name), **Rebuild**, then start. Remove the old experimental add-on entry to avoid confusion.

## Multiple ISM7 devices

Same pattern as upstream: use **additional ISM7 devices** in the add-on options. Details: [b3nn0 add-on README](https://github.com/b3nn0/hassio-addon-ism7mqtt/blob/main/README.md) (multi-instance section).

## Too many parameters / unstable ISM7

The ISM7 can be overwhelmed if you query hundreds of parameters. Mitigations (from upstream): reduce Wolf portal load, prefer Ethernet, trim `ism7-parameters-*.json`. See [b3nn0 README — “Important, if some entities are unavailable”](https://github.com/b3nn0/hassio-addon-ism7mqtt/blob/main/README.md).
