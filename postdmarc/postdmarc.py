import os
import requests

from .pm_exceptions import APIKeyMissingError


def setup():
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
                f"All methods require an API key. Please set the API key in either the "
                f"'POSTMARK_API_KEY' environment variable or in the {path} file."
            )
    session = requests.Session()
    session.headers.update({"X-Api-Token": PM_API_KEY})

    return session


if __name__ == "__main__":
    setup()
