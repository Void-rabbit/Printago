# Bambu Lab Printer API Research

This document summarizes findings on how to interact with Bambu Lab printers over the local network.

## Primary Method: MQTT over TLS

The most common method for local network interaction is via MQTT over TLS. Several community projects utilize this.

### Connection Details:
-   **MQTT Broker IP Address:** The local IP address of the printer.
-   **MQTT Broker Port:** `8883`
-   **Username:** `bblp`
-   **Password:** The `Access Code` found on the printer's touch screen (Settings -> Network).
-   **TLS:** Required. Self-signed certificates are used by the printer, so the MQTT client needs to be configured to handle this (e.g., by skipping certificate verification or trusting the specific self-signed certificate).
    -   In Python's `paho-mqtt`, this typically involves:
        ```python
        import ssl
        client.tls_set(tls_version=ssl.PROTOCOL_TLS, cert_reqs=ssl.CERT_NONE)
        client.tls_insecure_set(True)
        ```
-   **Printer Serial Number:** Required for constructing MQTT topics. Found on the printer's touch screen (Settings -> General).

### MQTT Topics:
-   **Subscription Topic (for receiving status):** `device/{SERIAL}/report`
    -   Replace `{SERIAL}` with the actual serial number of the printer.
    -   Messages on this topic are JSON payloads containing printer status and telemetry.
-   **Publish Topic (for initial request/command):** `device/{SERIAL}/request`
    -   Example payload to initiate data pushing (observed in community projects): `{"pushing": {"command": "start", "sequence_id": 0}}`. It's unclear if this is strictly necessary for *only* receiving data after an initial connection, but it's a common pattern. Other commands might be possible via this topic.

### Data Format (JSON Payload on `report` topic):
The `report` topic provides a JSON payload, typically under a top-level key like `"print"`.

Key fields observed in the `print` object:
-   `layer_num`: Current layer number.
-   `spd_lvl`: Speed level (e.g., 1: Silent, 2: Standard, 3: Sport, 4: Ludicrous).
-   `mc_remaining_time`: Estimated remaining print time in minutes.
-   `mc_percent`: Print progress percentage.
-   `nozzle_temper`: Current nozzle temperature.
-   `nozzle_target_temper`: Target nozzle temperature.
-   `bed_temper`: Current bed temperature.
-   `bed_target_temper`: Target bed temperature.
-   `vt_tray`: Details about the "virtual" or external spool.
    -   `vt_tray['cols'][0]`: Color hex code.
    -   `vt_tray['tray_type']`: Filament type.
-   `ams`: Object containing AMS status.
    -   `ams['tray_now']`: ID of the AMS tray currently in use.
    -   `ams['ams'][0]['tray']`: Array of AMS trays. Each tray object contains:
        -   `id`: Tray ID.
        -   `cols[0]`: Color hex code.
        -   `remain`: Percentage of filament remaining.
        -   `tray_sub_brands`: Filament sub-brand.
        -   `tray_type`: Filament type.

### Dependencies for Python:
-   `paho-mqtt`: For MQTT communication.
-   `webcolors`: (Optional, used in one example to convert RGB hex to color names).

## Cloud API:
-   There is also a cloud API (`https://api.bambulab.com/v1`) used by Bambu Studio and related tools.
-   Authentication for the cloud API is more complex, involving username/password and potentially MFA.
-   Projects like `ondrovic/bambulab-authentication-cli` explore this.
-   For direct local control and real-time status, MQTT is preferred.

## Camera Feed:
-   The printer's camera feed is accessible via RTSP or other streaming protocols.
-   The exact URL might depend on the printer model and firmware.
-   Typically something like `rtsp://<PRINTER_IP>/live` or an HTTP endpoint.
-   Authentication (using the access code) might be required.
-   The Bambu Lab Wiki mentions a "virtual camera" feature for OBS, which likely uses this stream. (https://wiki.bambulab.com/en/software/bambu-studio/virtual-camera)

## Open Questions/Further Investigation:
-   Full list of commands available via the `device/{SERIAL}/request` topic for controlling the printer (e.g., start/stop print, pause, resume).
-   Specific camera feed URLs (RTSP, MJPEG) and any associated authentication methods for different Bambu Lab printer models (X1C, P1P, P1S, A1 series).
-   Detailed structure of error codes and status messages returned via MQTT.
-   Possibility of programmatically retrieving the printer's `Access Code` and `Serial Number` after an initial setup (unlikely for initial discovery, but potentially for verification or re-establishment of connection). For initial setup, these must be retrieved from the printer's touchscreen.

## Relation to Current Application Implementation

The 3D Print Farm Manager application currently uses the findings from this research in the following ways:

*   **Printer Model:** The `Printer` data model in `app.py` (and subsequently `printers.json`) includes fields for `ip_address`, `serial_number`, and `access_code`. These fields are directly based on the information required for local MQTT communication with Bambu Lab printers as identified in this document.
*   **Mocked Status:** The "live status" displayed for printers in the web UI (e.g., on the `/printers/<printer_id>` page and the `/farm_dashboard`) is currently **mocked**. However, the structure of this mocked data (e.g., nozzle temperature, bed temperature, print progress) is inspired by the types of data fields (`nozzle_temper`, `bed_temper`, `mc_percent`, etc.) found in the JSON payloads on the `device/{SERIAL}/report` MQTT topic.
*   **Future Integration:** The collection of these details (`ip_address`, `serial_number`, `access_code`) is intended to facilitate future development of a real integration with Bambu Lab printers using their local MQTT API. The plan would be to implement an MQTT client within the Flask application (or a separate service it communicates with) that uses these stored credentials to connect to each printer, subscribe to its status topic, and potentially send commands.

This research document serves as a foundational guide for that future integration work.

## References (Community Projects)

The following community projects were instrumental in gathering information about the Bambu Lab local API:

-   **`MikeSiekkinen/BambuLabOBSOverlay`**: Python script for an OBS overlay, demonstrating MQTT connection, authentication, topic subscription, and payload parsing. (Primary source for MQTT details).
-   **`ondrovic/bambulab-authentication-cli`**: Python CLI tool for authenticating with the Bambu Lab *cloud* API. Useful for understanding general authentication patterns, though not directly for local MQTT.
-   **`THE-SIMPLE-MARK/bambu-node`**: A Node.js library for MQTT communication with Bambu Lab printers.
-   **`disconn3ct/bambu-proxy`**: An MQTT proxy for Bambu Lab printers, useful for inspecting messages.
-   **`ApanLoon/Bambu-Monitor`**: A tool to listen, log, and present messages from the Bambu Lab MQTT bus.
