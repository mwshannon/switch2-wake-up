# Switch 2 Wakeup automation

This repository contains two implementations of the same idea: sending a custom Bluetooth Low Energy advertising burst intended to wake a Switch 2.

This is research code, not a general-purpose solution. It is only a replay of BLE data captured from my own Joy-Cons, and it most likely only works with my own Switch setup because the hardcoded address values are taken from that capture. I do not have other Joy-Cons or other captured datasets to make this universal.

- `flipper_app/`: a Flipper Zero external app that sends one BLE burst when triggered from the device UI.
- `components/switch2_wake/`: a local ESPHome external component for ESP32 devices, with a matching button platform.

The Flipper app was mainly a proof of concept. The ESPHome component is the real solution for my own setup and actual use.

## Backstory

I got fed up with not being able to wake up my Switch 2 using my Switch 1 Pro Controller.

So I used an nRF BLE sniffer to capture what the Joy-Con sends when the `HOME` button is pressed and the Switch wakes up. This repository is the result of that reverse-engineering effort: a couple of small implementations that replay my captured Joy-Con BLE advertising behavior closely enough to wake my console. The Flipper version proved the idea; the ESPHome version is the one that actually solves the problem for me.

## Repository Layout

```text
.
├── components/
│   └── switch2_wake/   # ESPHome external component
├── examples/           # Example ESPHome YAML configs
├── flipper_app/        # Flipper Zero external app sources
└── scripts/
    └── sync_esphome_component.sh   # Development helper for syncing the local component
```

## Flipper Zero App

The Flipper app lives in `flipper_app/`:

- `application.fam`: Flipper app manifest
- `switch2_wake_test.c`: UI and BLE advertising logic

Behavior:

- Shows a simple screen with `ACTIVE` / `IDLE` state
- Pressing `OK` toggles state
- When toggled to `ACTIVE`, it sends a single short BLE advertising burst
- Pressing `BACK` exits the app

The app uses Flipper's extra beacon API and a fixed advertising payload/address.

## ESPHome Component

The ESPHome implementation lives in `components/switch2_wake/`.

It provides:

- A `switch2_wake:` component that manages BLE advertising
- A `button` platform named `switch2_wake` that triggers a burst on demand

Current configuration options:

- `ble_id`: ESPHome `esp32_ble` instance to attach to
- `duration`: advertising burst length, default `2000ms`
- `packet_count`: target number of packets during the burst, default `500`

The component:

- Configures a fixed raw BLE advertising payload
- Uses a fixed public MAC/base MAC
- Starts advertising when requested
- Stops advertising automatically after the configured burst duration

## Example Configs

Example ESPHome YAML files are in `examples/`.

- `switch2_wake_external.yaml`: recommended GitHub-based external component example

Recommended usage is to load the component directly from GitHub:

```yaml
external_components:
  - source:
      type: git
      url: https://github.com/tv/switch2-wake-up
    components: [switch2_wake]
```

`examples/secrets.yaml` is intended for local secrets and should be adjusted for your environment.

## Using the ESPHome Component

Typical use should be directly from GitHub as an ESPHome external component.

`scripts/sync_esphome_component.sh` exists for local development only. It copies `components/switch2_wake` to a remote ESPHome components directory over SSH so the component can be iterated on without pushing every change first.

Current defaults:

- Remote host: `root@homeassistant`
- Remote path: `/root/config/esphome/my_components`

Run:

```bash
./scripts/sync_esphome_component.sh
```

Adjust the variables at the top of the script if your Home Assistant or ESPHome host uses a different location.

## Notes

- This repository currently focuses on source layout and implementation, not full build automation.
- The BLE payload, MAC/base MAC, timing, and packet count are all tailored to this specific use case.
- This is not a universal implementation of Switch wake behavior. It replays my own captured Joy-Con data, and I do not have enough hardware data to generalize it further.
- If you want to use this with another console, you should expect to inspect and replace the hardcoded address and payload values.
