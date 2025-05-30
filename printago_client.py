import requests
import json
import logging
import os # For token storage path

logger = logging.getLogger(__name__)

class PrintagoAPIClient:
    def __init__(self, api_key, store_id, base_url="https://api.printago.io/v1"):
        self.api_key = api_key
        self.store_id = store_id
        self.base_url = base_url
        self.headers = {
            "Authorization": f"ApiKey {self.api_key}",
            "x-printago-storeid": self.store_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        # TODO: Consider adding a User-Agent header

    def _request(self, method, endpoint, params=None, json_data=None):
        url = self.base_url + endpoint
        logger.info(f"Request: {method} {url}")
        logger.debug(f"Headers: {self.headers}")
        if params:
            logger.debug(f"Params: {params}")
        if json_data:
            logger.debug(f"JSON Data: {json.dumps(json_data, indent=2)}")

        try:
            response = requests.request(method, url, headers=self.headers, params=params, json=json_data, timeout=30) # Added timeout
            logger.info(f"Response Status: {response.status_code}")

            if response.status_code == 204: # No Content
                return None

            response.raise_for_status() # Raises HTTPError for 4xx/5xx status codes

            # Handle cases where response might be empty but still 2xx
            if not response.content:
                return None

            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e} - Response: {e.response.text if e.response else 'No response text'}")
            # Optionally, parse error response from API if it's JSON
            try:
                error_details = e.response.json()
                logger.error(f"API Error Details: {error_details}")
            except ValueError: # Includes JSONDecodeError
                pass # No JSON error details or not a JSON response
            raise # Re-raise the exception after logging
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error occurred: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error occurred: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"An unexpected error occurred with the request: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e} - Response Text: {response.text}")
            raise ValueError(f"Failed to decode JSON response: {response.text}") # Raise a ValueError to signal this

    # --- Read-Only Methods (from previous implementation, verified paths) ---
    def get_parts(self):
        return self._request("GET", "/v1/parts")

    def get_part(self, part_id: str):
        if not part_id:
            logger.warning("get_part called with empty part_id")
            return None
        return self._request("GET", f"/v1/parts/{part_id}")

    def get_printers(self):
        return self._request("GET", "/v1/printers")

    def get_printer(self, printer_id: str):
        if not printer_id:
            logger.warning("get_printer called with empty printer_id")
            return None
        return self._request("GET", f"/v1/printers/{printer_id}")

    def get_printer_stats(self, printer_ids: list[str] = None):
        # Based on OpenAPI: GET /v1/printers/stats and GET /v1/printers/stats/{ids}
        if printer_ids and len(printer_ids) > 0:
            ids_param = ",".join(printer_ids)
            endpoint = f"/v1/printers/stats/{ids_param}"
        else:
            endpoint = "/v1/printers/stats"
        return self._request("GET", endpoint)

    def get_print_jobs(self, status: str = None, printerId: str = None): # Corrected param name
        params = {}
        if status:
            params["status"] = status
        if printerId:
            params["printerId"] = printerId # Corrected key
        return self._request("GET", "/v1/print-jobs", params=params) # Corrected endpoint

    def get_profiles(self):
        # Based on OpenAPI: GET /v1/profiles
        return self._request("GET", "/v1/profiles")

    def get_skus(self):
        # Based on OpenAPI: GET /v1/skus
        return self._request("GET", "/v1/skus")

    # --- New/Extended Methods ---

    # Part Management
    def create_part(self, part_data: dict):
        # Body schema: PartInsert
        return self._request("POST", "/v1/parts", json_data=part_data)

    def update_part(self, part_id: str, part_data: dict):
        # Body schema: PartInsert (OpenAPI spec may need clarification for PATCH, often it's Partial<PartInsert>)
        if not part_id:
            logger.warning("update_part called with empty part_id")
            return None
        return self._request("PATCH", f"/v1/parts/{part_id}", json_data=part_data)

    def delete_part(self, part_id: str):
        if not part_id:
            logger.warning("delete_part called with empty part_id")
            return None
        return self._request("DELETE", f"/v1/parts/{part_id}")

    def delete_parts_bulk(self, part_ids: list[str]):
        # Request body is an array of strings (part IDs)
        if not part_ids:
            logger.warning("delete_parts_bulk called with empty part_ids list")
            return []
        return self._request("DELETE", "/v1/parts", json_data=part_ids)

    # Printer Configuration
    def update_printer_settings(self, printer_id: str, settings_data: dict):
        # Body schema: PartialPrinterUpdate
        if not printer_id:
            logger.warning("update_printer_settings called with empty printer_id")
            return None
        return self._request("PATCH", f"/v1/printers/{printer_id}", json_data=settings_data)

    def set_printer_config_bulk(self, config_data: dict):
        # Body schema: SetProviderConfig
        return self._request("PATCH", "/v1/printers/set-config", json_data=config_data)

    def rename_printer(self, printer_id: str, name: str):
        # Body schema: RenamePrinterOptions
        if not printer_id:
            logger.warning("rename_printer called with empty printer_id")
            return None
        return self._request("PATCH", f"/v1/printers/{printer_id}/rename", json_data={"name": name})

    # Print Job Management
    def get_print_job(self, job_id: str):
        if not job_id:
            logger.warning("get_print_job called with empty job_id")
            return None
        return self._request("GET", f"/v1/print-jobs/{job_id}")

    def create_build(self, build_config: dict):
        # Body schema: BuildConfig
        return self._request("POST", "/v1/builds", json_data=build_config)

    def update_print_job(self, job_id: str, job_data: dict):
        # Body schema: PartialPrintJobInsert
        if not job_id:
            logger.warning("update_print_job called with empty job_id")
            return None
        return self._request("PATCH", f"/v1/print-jobs/{job_id}", json_data=job_data)

    def _operate_on_print_jobs(self, operation: str, job_ids: list[str]):
        if not job_ids:
            logger.warning(f"_operate_on_print_jobs ({operation}) called with empty job_ids list")
            return []
        # Body: {"printJobIds": job_ids}
        return self._request("PATCH", f"/v1/print-jobs/{operation}", json_data={"printJobIds": job_ids})

    def pause_print_jobs(self, job_ids: list[str]):
        return self._operate_on_print_jobs("pause", job_ids)

    def cancel_print_jobs(self, job_ids: list[str]):
        return self._operate_on_print_jobs("cancel", job_ids)

    def resume_print_jobs(self, job_ids: list[str]):
        return self._operate_on_print_jobs("resume", job_ids)

    # Folder Management
    def list_folders(self, folder_type: str = None):
        if folder_type:
            endpoint = f"/v1/folders/by-type/{folder_type}"
        else:
            endpoint = "/v1/folders"
        return self._request("GET", endpoint)

    def create_folder(self, name: str, type: str, parent_id: str = None):
        # Body schema: CreateFolderRequest
        payload = {"name": name, "type": type}
        if parent_id is not None: # Allow parent_id to be explicitly null or a string
            payload["parentId"] = parent_id
        return self._request("POST", "/v1/folders", json_data=payload)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # TODO: Load API_KEY and STORE_ID from environment variables or a secure config file.
    # For now, using the values provided in the initial issue for testing.
    API_KEY = "uw9cgpqf3cav0jt68iuhroqmpnpzylgyd9v1hnh4qj1dgxc9u8avxvrg0dub4jj10q1z9uy6"
    STORE_ID = "jma9q6h3iahb9czvy0ton79n"

    if not API_KEY or API_KEY == "YOUR_PRINTAGO_API_KEY" or not STORE_ID or STORE_ID == "YOUR_PRINTAGO_STORE_ID":
        logger.error("API_KEY or STORE_ID not set. Please set them for testing.")
    else:
        client = PrintagoAPIClient(api_key=API_KEY, store_id=STORE_ID)

        try:
            print("\n--- Getting Printers ---")
            printers = client.get_printers()
            if printers:
                logger.info(f"Found {len(printers)} printers.")
                # for printer in printers:
                #     print(f"  Printer ID: {printer.get('id')}, Name: {printer.get('name')}, Status: {printer.get('isOnline')}")
                if len(printers) > 0:
                    first_printer_id = printers[0].get('id')
                    print(f"--- Getting details for first printer: {first_printer_id} ---")
                    printer_details = client.get_printer(first_printer_id)
                    # if printer_details:
                        # print(json.dumps(printer_details, indent=2))

                printer_ids_for_stats = [p.get('id') for p in printers if p.get('id')][:2] # Get stats for first two
                if printer_ids_for_stats:
                    print(f"--- Getting stats for printers: {printer_ids_for_stats} ---")
                    stats = client.get_printer_stats(printer_ids_for_stats)
                    # if stats:
                        # print(json.dumps(stats, indent=2))
                else:
                    print("--- Getting all printer stats (no specific IDs) ---")
                    all_stats = client.get_printer_stats()
                    # if all_stats:
                        # print(json.dumps(all_stats, indent=2))


            print("\n--- Getting Parts ---")
            parts = client.get_parts()
            if parts:
                logger.info(f"Found {len(parts)} parts.")
                # for part in parts:
                #     print(f"  Part ID: {part.get('id')}, Name: {part.get('name')}")

            print("\n--- Getting Print Jobs (pending) ---")
            pending_jobs = client.get_print_jobs(status="pending")
            if pending_jobs:
                logger.info(f"Found {len(pending_jobs)} pending print jobs.")
                # for job in pending_jobs:
                #     print(f"  Job ID: {job.get('id')}, Part Name: {job.get('partName')}, Status: {job.get('status')}")

            print("\n--- Getting Profiles ---")
            profiles = client.get_profiles()
            if profiles:
                logger.info(f"Found {len(profiles)} profiles.")

            print("\n--- Getting SKUs ---")
            skus = client.get_skus()
            if skus:
                logger.info(f"Found {len(skus)} SKUs.")

            # --- Example Write Operations (Commented Out By Default) ---
            # print("\n--- Example: Creating a part ---")
            # # IMPORTANT: Fields for PartInsert need to be accurate as per OpenAPI spec
            # # This is a minimal example and might be missing required fields.
            # new_part_data = {
            #    "name": "Test API Part - Delete Me",
            #    "type": "stl", # one of ["scad", "stl", "step", "3mf", "gcode3mf"]
            #    "fileUris": ["http://example.com/some_part.stl"], # Placeholder URI
            #    "fileHashes": ["dummymd5hashplaceholder123"],     # Placeholder hash
            #    # "description": "A part created via API for testing.",
            #    # "parameters": [],
            #    # "printTags": {},
            #    # "allowedFilamentTypes": ["PLA"],
            # }
            # # created_part = client.create_part(new_part_data) # UNCOMMENT TO TEST
            # # if created_part:
            # #    logger.info(f"Created part: {created_part.get('id')} - {created_part.get('name')}")
            # #    # print(json.dumps(created_part, indent=2))
            # #
            # #    # Example: Update the part just created
            # #    print(f"--- Example: Updating part {created_part.get('id')} ---")
            # #    updated_part_data = {"description": "Updated description."}
            # #    updated_part = client.update_part(created_part.get('id'), updated_part_data)
            # #    if updated_part:
            # #        logger.info(f"Updated part description: {updated_part.get('description')}")
            # #
            # #    # Example: Deleting the part just created (use with caution)
            # #    print(f"--- Example: Deleting part {created_part.get('id')} ---")
            # #    delete_response = client.delete_part(created_part.get('id')) # UNCOMMENT TO TEST
            # #    if delete_response is not None: # Delete might return 204 No Content or an object
            # #        logger.info(f"Delete part response: {delete_response}")
            # #    else:
            # #        logger.info(f"Part {created_part.get('id')} likely deleted (204 No Content).")


            # print("\n--- Example: Creating a folder ---")
            # # new_folder_data = {"name": "API Test Folder", "type": "part"}
            # # created_folder = client.create_folder(name="API Test Parts", type="part", parent_id=None) # UNCOMMENT TO TEST
            # # if created_folder:
            # #    logger.info(f"Created folder: {created_folder.get('id')} - {created_folder.get('name')}")

        except requests.exceptions.HTTPError as e:
            logger.error(f"CIVIC_API_CLIENT_EXAMPLE_HTTP_ERROR: {e}")
        except Exception as e:
            logger.error(f"CIVIC_API_CLIENT_EXAMPLE_ERROR: An unexpected error occurred in example usage: {e}", exc_info=True)
