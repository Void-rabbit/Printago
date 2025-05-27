# Printago API Research (and its relation to Bambu Lab Cloud Focus)

This document originally summarized findings on how to interact with the Printago API. However, recent development efforts have shifted focus towards integrating with the **Bambu Lab Cloud API** for user authentication and printer discovery within the "Printago Manager" (which is now more accurately a "Bambu Cloud Printer Manager" in its current iteration).

This document will retain the original Printago API research for historical context and potential future re-evaluation, but will also clarify the current project's direction.

## Original Printago API Research

### API Type and Purpose (Printago)

*   **Nature:** Server-to-Server API.
*   **Authentication Method:** Static API Key associated with a specific Printago Store ID.
*   **Primary Use Case:** Allows an external application to act as a client for a *specific Printago store*. This is not designed for end-users to log in with their personal Printago accounts.

### Authentication (Printago)

As per `https://docs.printago.io/docs/api/authentication`:

*   The API uses two main headers for authentication:
    1.  `authorization: ApiKey YOUR_API_KEY`
        *   Replace `YOUR_API_KEY` with the actual API key provided by Printago.
    2.  `x-printago-storeid: YOUR_STORE_ID`
        *   Replace `YOUR_STORE_ID` with the specific Store ID the API key is associated with.

*   **API Key Provisioning (Printago):**
    *   API keys are not self-serve. They must be obtained by contacting Printago support directly.
    *   This manual process implies that each instance of our application intending to connect to a specific Printago store would need its own unique API Key and corresponding Store ID.

### Supported Operations (Printago - To Be Verified)

The specific operations supported by the Printago API (once authenticated) need to be determined by reviewing their API specification, typically found at `https://docs.printago.io/docs/api/Specification`.

Expected operations would likely include:

*   Listing Parts, Managing Print Queues, Viewing Printers, Order Management (all specific to the configured Printago store).

**Note:** A detailed review of the Printago API specification is required to confirm the exact endpoints, request/response formats, and capabilities.

### Limitations for User-Centric Login (Printago)

*   **Store-Specific, Not User-Specific:** This API is designed for server-to-server integration with a specific Printago Store ID. It does **not** support individual users logging in with their personal Printago accounts.
*   **Application-Level Integration:** The application, when integrating with Printago, would be configured with a single API Key and Store ID.

## Current Project Focus: Bambu Lab Cloud Integration

The "Printago Manager" desktop application, in its current development phase, is primarily focused on integrating with the **Bambu Lab Cloud API**. This involves:

1.  **User Authentication:** Users log in with their personal Bambu Lab cloud accounts (username/password).
2.  **Printer Discovery:** After successful authentication, the application fetches a list of printers registered to that Bambu Lab account.
3.  **Token Management:** Access tokens obtained from Bambu Lab cloud authentication are stored locally (e.g., in `~/.printago_manager/cloud_auth.json`) to maintain sessions and make authenticated API calls.

This functionality is implemented in `bambu_cloud_client.py` and integrated into `desktop_app.py`.

## Reconciling "Printago Manager" Name with Bambu Lab Focus

*   The application name "Printago Manager" might become a misnomer if the primary integration remains with Bambu Lab Cloud.
*   **Consideration for future:**
    *   Rename the application to something like "Cloud Printer Manager" or "Bambu Cloud Connect."
    *   Or, retain the name if future plans include re-introducing or adding Printago API integration as a distinct, separate feature (e.g., allowing users to connect to *either* their Bambu Lab account *or* a specific Printago Store).

For now, the development is proceeding with Bambu Lab cloud integration as the active path, using the existing "Printago Manager" name for the application shell. The `printago_api_research.md` serves as a reference for a potential, distinct Printago store integration feature.
