"""Provide a Python wrapper for the Postmark DMARC API."""
import os
import requests

from . import pdm_exceptions as errors


class PostDmarc:
    """Connection object to the Postmark DMARC API."""

    def __init__(self):
        """Initialize object with default values."""
        self.api_key = self.get_api_key()
        self.endpoint = "https://dmarc.postmarkapp.com"
        self.session = requests.Session()
        self.session.headers.update(
            {"X-Api-Token": self.api_key, "Accept": "application/json"}
        )

    def get_api_key(self):
        """Set the API key and create the session."""
        # Try to load the API key from the environment variable
        PM_API_KEY = os.environ.get("POSTMARK_API_KEY", None)

        if PM_API_KEY is None:
            try:
                # Try to load the API key from the "PM_API.key" file
                path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "PM_API.key"
                )
                with open(path, "r") as f:
                    PM_API_KEY = f.read()
            except FileNotFoundError:
                raise errors.APIKeyMissingError(
                    f"All methods require an API key. Please set the API key in either "
                    f"the 'POSTMARK_API_KEY' environment variable or in "
                    f"the {path} file."
                )
        return PM_API_KEY

    def check_response(self, response):
        """Check the status code of the API response.

        200 — OK
            Your request was fulfilled.
        204 — No Content
            Your request was fulfilled, the response body is empty.
        303 — See Other
            Your request is being redirected to a different URI.
        400 — Bad Request
            Something with your request isn’t quite right, this could be malformed JSON.
        422 — Unprocessable Entity
            Your request has failed validations.
        500 — Internal Server Error
            Our servers have failed to process your request.

        """
        mapping = {
            200: None,
            204: None,
            303: None,
            400: errors.BadRequestError,
            404: errors.PageNotFoundError,
            422: errors.UnprocessableEntityError,
            500: errors.InternalServerError,
        }

        try:
            return mapping[response.status_code]
        except KeyError:
            return errors.UnrecognizedStatusCodeError

    def create_record(self, email, domain):
        """Create a new DMARC record for a given domain and email."""
        endpoint_path = "/records"
        body = {"email": email, "domain": domain}
        del self.session.headers["X-Api-Token"]
        response = self.session.post(self.endpoint + endpoint_path, json=body)
        self.session.headers.update({"X-Api-Token": self.api_key})
        self.check_response(response)
        return response.json()

    def get_record(self):
        """Get a record’s information."""
        pass

    def update_record(self):
        """Update a record’s information."""
        self.session.headers.update({"Content-Type": "application/json"})
        pass

    def get_dns_snippet(self):
        """Get generated DMARC DNS record name and value."""
        pass

    def verify_dns(self):
        """Verify if your DMARC DNS record exists."""
        pass

    def delete_record(self):
        """Delete a record.

        Deleting a record will stop processing data for this domain.
        The email associated with this record will also be unsubscribed from the DMARC
        weekly digests for this domain only.
        """
        pass

    def list_reports(self):
        """List all received DMARC reports for a given domain with the ability to filter
        results by a single date or date range."""
        pass

    def get_report(self):
        """Load full DMARC report details.

        Load full DMARC report details as a raw DMARC XML document
        or as our own JSON representation.
        """
        pass

    def recover_token(self):
        """Initiate API token recovery for a domain.

        This endpoint is public and doesn't require authentication.
        """
        self.session.headers.update({"Content-Type": "application/json"})
        pass

    def rotate_token(self):
        """Generate a new API token and replace your existing one with it."""
        pass


if __name__ == "__main__":
    pdm_obj = PostDmarc()
