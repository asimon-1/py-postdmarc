import os
import requests

from .pdm_exceptions import APIKeyMissingError


class PostDmarc:
    def __init__(self):
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
                raise APIKeyMissingError(
                    f"All methods require an API key. Please set the API key in either "
                    f"the 'POSTMARK_API_KEY' environment variable or in "
                    f"the {path} file."
                )
        return PM_API_KEY

    def base_method(self, body):
        pass

    def create_record(self):
        self.session.headers.update({"Content-Type": "application/json"})
        pass

    def get_record(self):
        pass

    def update_record(self):
        self.session.headers.update({"Content-Type": "application/json"})
        pass

    def get_dns_snippet(self):
        pass

    def verify_dns(self):
        pass

    def delete_record(self):
        pass

    def list_reports(self):
        pass

    def get_report(self):
        pass

    def recover_token(self):
        self.session.headers.update({"Content-Type": "application/json"})
        pass

    def rotate_token(self):
        pass


if __name__ == "__main__":
    pdm = PostDmarc()
