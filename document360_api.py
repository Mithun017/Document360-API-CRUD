import requests
import json
import sys
from typing import Dict, Any, Optional
from uuid import uuid4

class Document360Model:
    """Handles interactions with the Document360 API."""
    
    def __init__(self, api_token: str):
        self.base_url = "https://apihub.document360.io/v2/Drive/Folders"
        self.headers = {
            "api_token": api_token,
            "Content-Type": "application/json"
        }
        self.folder_id = None

    def get_all_folders(self) -> tuple[Optional[Dict[str, Any]], Optional[requests.Response]]:
        """Fetch all drive folders using GET method."""
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):  
                    return data, response
                return None, response
            return None, response
        except requests.RequestException as e:
            return None, None

    def create_folder(self, folder_name: str) -> tuple[Optional[str], Optional[requests.Response]]:
        """Create a new folder using POST method."""
        body = {"name": folder_name}
        try:
            response = requests.post(self.base_url, headers=self.headers, json=body, timeout=10)
            if response.status_code == 201:
                response_data = response.json()
                if 'id' in response_data:  
                    self.folder_id = response_data['id']
                    return self.folder_id, response
                return None, response
            return None, response
        except requests.RequestException as e:
            return None, None

    def update_folder(self, folder_id: str, new_name: str) -> tuple[bool, Optional[requests.Response]]:
        """Update folder name using PUT method."""
        if not folder_id:
            return False, None
        url = f"{self.base_url}/{folder_id}"
        body = {"name": new_name}
        try:
            response = requests.put(url, headers=self.headers, json=body, timeout=10)
            return response.status_code == 200, response
        except requests.RequestException as e:
            return False, None

    def delete_folder(self, folder_id: str) -> tuple[bool, Optional[requests.Response]]:
        """Delete a folder using DELETE method."""
        if not folder_id:
            return False, None
        url = f"{self.base_url}/{folder_id}"
        try:
            response = requests.delete(url, headers=self.headers, timeout=10)
            return response.status_code == 204, response
        except requests.RequestException as e:
            return False, None

class Document360View:
    """Handles console output for the Document360 API application."""
    
    def log_request(self, method: str, url: str, headers: Dict[str, str], body: Optional[Dict] = None) -> None:
        """Log request details."""
        print(f"\n=== {method} Request ===")
        print(f"URL: {url}")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        if body:
            print(f"Body: {json.dumps(body, indent=2)}")

    def log_response(self, response: Optional[requests.Response]) -> None:
        """Log response details."""
        print(f"\n=== Response ===")
        if response is None:
            print("No response received (request failed)")
        else:
            print(f"Status Code: {response.status_code}")
            try:
                print(f"Body: {json.dumps(response.json(), indent=2)}")
            except ValueError:
                print(f"Body: {response.text}")
        print("================\n")

    def show_success(self, message: str) -> None:
        """Display a success message."""
        print(f"Success: {message}")

    def show_error(self, message: str, status_code: Optional[int] = None, expected_status: Optional[int] = None, error_detail: Optional[str] = None) -> None:
        """Display an error message."""
        print(f"Error: {message}")
        if status_code is not None and expected_status is not None:
            print(f"Expected status {expected_status}, got {status_code}")
        if error_detail:
            print(f"Error Details: {error_detail}")

class Document360Presenter:
    """Coordinates CRUD operations between Model and View."""
    
    def __init__(self, model: Document360Model, view: Document360View):
        self.model = model
        self.view = view

    def get_all_folders(self) -> Optional[Dict[str, Any]]:
        """Execute GET operation to fetch all folders."""
        self.view.show_success("Task 1: Fetching all folders")
        self.view.log_request("GET", self.model.base_url, self.model.headers)
        data, response = self.model.get_all_folders()
        self.view.log_response(response)
        if data is None:
            error_detail = None
            if response:
                try:
                    error_detail = response.json().get('error', 'No error details provided')
                except ValueError:
                    error_detail = response.text
            self.view.show_error("Failed to fetch folders", response.status_code if response else None, 200, error_detail)
            return None
        return data

    def create_folder(self, folder_name: str) -> Optional[str]:
        """Execute POST operation to create a new folder."""
        self.view.show_success("Task 2: Creating a new folder")
        self.view.log_request("POST", self.model.base_url, self.model.headers, {"name": folder_name})
        folder_id, response = self.model.create_folder(folder_name)
        self.view.log_response(response)
        if folder_id is None:
            error_detail = None
            if response:
                try:
                    error_detail = response.json().get('error', 'No error details provided')
                except ValueError:
                    error_detail = response.text
            self.view.show_error("Failed to create folder", response.status_code if response else None, 201, error_detail)
            return None
        self.view.show_success(f"Folder '{folder_name}' created with ID: {folder_id}")
        return folder_id

    def update_folder(self, folder_id: str, new_name: str) -> bool:
        """Execute PUT operation to update folder name."""
        self.view.show_success("Task 3: Updating folder name")
        self.view.log_request("PUT", f"{self.model.base_url}/{folder_id}", self.model.headers, {"name": new_name})
        success, response = self.model.update_folder(folder_id, new_name)
        self.view.log_response(response)
        if not success:
            error_detail = None
            if response:
                try:
                    error_detail = response.json().get('error', 'No error details provided')
                except ValueError:
                    error_detail = response.text
            self.view.show_error("Failed to update folder", response.status_code if response else None, 200, error_detail)
            return False
        self.view.show_success(f"Folder ID {folder_id} renamed to '{new_name}'")
        return True

    def delete_folder(self, folder_id: str) -> bool:
        """Execute DELETE operation to delete a folder."""
        self.view.show_success("Task 4: Deleting folder")
        self.view.log_request("DELETE", f"{self.model.base_url}/{folder_id}", self.model.headers)
        success, response = self.model.delete_folder(folder_id)
        self.view.log_response(response)
        if not success:
            error_detail = None
            if response:
                try:
                    error_detail = response.json().get('error', 'No error details provided')
                except ValueError:
                    error_detail = response.text
            self.view.show_error("Failed to delete folder", response.status_code if response else None, 204, error_detail)
            return False
        self.view.show_success(f"Folder ID {folder_id} deleted")
        return True

def main():
    """Main function to execute CRUD operations using MVP pattern."""
    api_token = "M1XbCrQnV47mHjZcYnpsUPR3R1DiJ7/jGwTBQO2MiNjXtg5alNTLp0H0yB1URuaNMgPiQU1cew270dZK6ZB8hRSChDm2vRqg0WSuplRVkqb0XOsbQJG4J7ev81mnd9wCrCpaOurY2KyPIJB5b3K+DQ=="  # Replace with actual Document360 API token
    model = Document360Model(api_token)
    view = Document360View()
    presenter = Document360Presenter(model, view)
    
    folders = presenter.get_all_folders()
    if not folders:
        presenter.view.show_error("Failed to fetch folders. Exiting.")
        sys.exit(1)
    
    folder_name = f"TestFolder_{str(uuid4())[:8]}"
    folder_id = presenter.create_folder(folder_name)
    if not folder_id:
        presenter.view.show_error("Failed to create folder. Exiting.")
        sys.exit(1)
    
    new_folder_name = f"UpdatedFolder_{str(uuid4())[:8]}"
    if not presenter.update_folder(folder_id, new_folder_name):
        presenter.view.show_error("Failed to update folder. Exiting.")
        sys.exit(1)
    
    if not presenter.delete_folder(folder_id):
        presenter.view.show_error("Failed to delete folder. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()