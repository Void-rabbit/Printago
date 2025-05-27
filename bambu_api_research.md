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
-   For direct local control and real-time status, MQTT is preferred for low-latency operations. The Cloud API can complement this with account-level features.

## Cloud API (User Account Authentication & Management)

This section details the cloud-based API provided by Bambu Lab, primarily used for user account authentication and potentially managing printers linked to an account.

-   **API Base URL:** `https://api.bambulab.com/v1`
-   **Authentication Method:**
    -   Uses username (email) and password.
    -   Supports Multi-Factor Authentication (MFA).
    -   Successful authentication yields an access token (and potentially a refresh token).
-   **Reference Implementation:** The `ondrovic/bambulab-authentication-cli` GitHub repository provides a Python-based command-line tool that demonstrates this authentication flow. This tool is a key resource for understanding the process.
-   **Client Metadata:** Successful authentication and subsequent API calls may require specific client metadata in request headers (e.g., `User-Agent`, `Bambu_Client_Name`, `Bambu_Client_Type`, `Bambu_Client_Version`). These should mimic official clients like OrcaSlicer or Bambu Studio, as observed in the `ondrovic/bambulab-authentication-cli` tool's configuration (`.env.example`).

### Post-Authentication Endpoints (To Be Investigated):

Once authenticated, the access token can be used to access further endpoints. The exact structure and capabilities of these endpoints require more detailed investigation, potentially by observing network traffic from official Bambu Lab applications (Bambu Studio, Bambu Handy) or by finding more detailed API documentation. Hypothetical endpoints could include:

*   `/user/printers`: To list printers associated with the authenticated user's account.
*   `/printers/{device_id}/status`: To get the status of a specific printer linked to the account.
*   `/printers/{device_id}/print_profiles`: To manage print profiles stored in the cloud for a specific printer.
*   `/printers/{device_id}/commands`: To send commands (e.g., start print from cloud-stored file, pause, stop) to a printer.

**Note:** "These endpoints are speculative and require further investigation, possibly by observing traffic from official Bambu Lab applications (Bambu Studio, Bambu Handy) after successful authentication via the method demonstrated by `bambulab-authentication-cli`."

### Token Management:

*   The authentication process yields an access token and potentially a refresh token.
*   These tokens should be securely stored by the client application (like our 3D Print Farm Manager) for making subsequent authenticated API calls.
*   The `ondrovic/bambulab-authentication-cli` tool, for example, saves these tokens to a local JSON file (`auth.json` by default).
*   Access tokens are typically short-lived, and refresh tokens (if provided) would be used to obtain new access tokens without requiring the user to re-enter their credentials.

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

## Distinction Between Local MQTT API and Cloud API

It's crucial to distinguish between the two primary APIs discussed:

1.  **Local MQTT API:**
    *   **Purpose:** Direct control and real-time status monitoring of a printer on the local network (LAN).
    *   **Authentication:** Uses the printer's IP address, serial number, and the "Access Code" found on the printer's screen.
    *   **Pros:** Low latency, does not require internet connectivity once set up (for local operations).
    *   **Cons:** Limited to local network access; does not provide access to account-level features or printers outside the LAN.

2.  **Cloud API (User Account Authentication & Management):**
    *   **Purpose:** Account-level operations, such as listing printers registered to a user's Bambu Lab account, potentially starting prints from cloud-stored files, and managing printer settings remotely.
    *   **Authentication:** Uses Bambu Lab user account credentials (username/password, MFA), resulting in an access token.
    *   **Pros:** Access printers from anywhere with an internet connection; manage account-level settings and features.
    *   **Cons:** Higher latency compared to local MQTT; dependent on internet connectivity and Bambu Lab's cloud services.

## Relation to Current and Future Application Implementation

The 3D Print Farm Manager application's integration with Bambu Lab printers can be envisioned in phases:

*   **Current State (Phase 1 - Local Focus):**
    *   The `Printer` data model in `app.py` (and `printers.json`) stores `ip_address`, `serial_number`, and `access_code`. This is tailored for the **Local MQTT API**.
    *   Live status display is currently **mocked**, but the data fields are inspired by MQTT payloads.
    *   The primary goal with these fields was to prepare for direct local MQTT communication for real-time status and control.

*   **Future Integration Plan (Phase 2 - Hybrid Approach):**
    *   **Local MQTT API:** Will remain the primary method for real-time status updates and direct control of printers available on the local network. This ensures low latency and continued operation even if cloud services are unavailable.
    *   **Cloud API:** Will be integrated to:
        *   Allow users to authenticate with their Bambu Lab cloud accounts.
        *   Fetch a list of printers registered to their account, potentially pre-filling or allowing users to select printers to add to the farm manager.
        *   Access cloud-based features if available and relevant (e.g., print history, cloud-stored print profiles, initiating prints from cloud-sliced files).
        *   The application would need to securely store and manage the access/refresh tokens obtained from the Cloud API authentication.
    *   This hybrid approach would offer the benefits of both local responsiveness and cloud-based account management and accessibility.

## API Endpoint Verification (October 2024)

An attempt was made to verify the exact Cloud API endpoints for authentication and printer listing.

*   **Authentication Endpoint (`AUTH_ENDPOINT`):**
    *   The `ondrovic/bambulab-authentication-cli` repository's `.env.example` specifies `BAMBU_API_URL=https://api.bambulab.com/v1`.
    *   While the README doesn't explicitly state the full path for the initial username/password POST request, the common pattern and the CLI's structure suggest that `https://api.bambulab.com/v1/user/login` is the correct endpoint for the initial authentication attempt. The separate `BAMBU_MFA_URL` (`https://bambulab.com/api/sign-in/tfa`) is used for subsequent MFA steps.
    *   **Conclusion:** `AUTH_ENDPOINT` in `bambu_cloud_client.py` remains `https://api.bambulab.com/v1/user/login`. This is a reasonably confirmed endpoint for the initial step of authentication.

*   **Printers List Endpoint (`PRINTERS_ENDPOINT`):**
    *   The `ondrovic/bambulab-authentication-cli` tool focuses solely on authentication and does not provide functionality or examples for listing printers or other post-authentication API calls.
    *   Targeted web searches (Google, GitHub discussions) for "bambu lab cloud api get printers endpoint", "bambu lab api list devices after login", and similar queries did not yield definitive, officially documented endpoints for listing printers associated with a user account.
    *   Some community discussions hint at endpoints like `/user/device` or `/device` but without strong confirmation or detailed examples.
    *   **Conclusion:** The endpoint for fetching a list of printers after login remains **unconfirmed and speculative**. The current `PRINTERS_ENDPOINT = API_BASE_URL + "/user/device"` in `bambu_cloud_client.py` is an educated guess based on limited community information.
    *   **Blocker:** Without a confirmed endpoint for listing printers, the "printer discovery" feature in the desktop application cannot be reliably implemented beyond its current placeholder status. Further investigation, potentially by inspecting network traffic from official Bambu Lab applications, is required to identify this endpoint. **This is the primary reason the desktop application currently cannot display a list of printers after Bambu Cloud login.**

This research document serves as a foundational guide for both local MQTT and Cloud API integration efforts, noting current uncertainties.

### Camera Feed Access (Not Integrated in UI)

*   **General Access:** Bambu Lab printers typically provide a camera feed accessible via RTSP.
*   **Common URL Pattern:** `rtsp://<PRINTER_IP>/live` (where `<PRINTER_IP>` is the local IP address of the printer).
*   **Authentication:** Accessing the RTSP stream usually requires the printer's "Access Code" (the same one used for local MQTT). The exact method of providing these credentials can vary by RTSP client (e.g., `rtsp://user:password@host/path` or prompted by the client).
*   **Bambu Studio/Handy:** These official applications use this stream for live video.
*   **Current Application State:** While this information is known, the camera feed is **not integrated** into the current PySide2 desktop UI. The "View Printer Details" section in the UI mockups includes a placeholder for a camera feed, but its implementation was contingent on resolving more fundamental UI construction issues.

## References (Community Projects)

The following community projects were instrumental in gathering information about the Bambu Lab local API:

-   **`MikeSiekkinen/BambuLabOBSOverlay`**: Python script for an OBS overlay, demonstrating MQTT connection, authentication, topic subscription, and payload parsing. (Primary source for MQTT details).
-   **`ondrovic/bambulab-authentication-cli`**: Python CLI tool for authenticating with the Bambu Lab *cloud* API. Useful for understanding general authentication patterns, though not directly for local MQTT.
-   **`THE-SIMPLE-MARK/bambu-node`**: A Node.js library for MQTT communication with Bambu Lab printers.
-   **`disconn3ct/bambu-proxy`**: An MQTT proxy for Bambu Lab printers, useful for inspecting messages.
-   **`ApanLoon/Bambu-Monitor`**: A tool to listen, log, and present messages from the Bambu Lab MQTT bus.
