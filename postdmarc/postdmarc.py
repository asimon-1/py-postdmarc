"""Provide a Python wrapper for the Postmark DMARC API.

See the documentation at https://dmarc.postmarkapp.com/api/
"""
import json
import os
from collections import defaultdict
from datetime import datetime
from typing import DefaultDict, NamedTuple, Optional, Type, Union

import fire
import requests
from dateparser import parse

from . import pdm_exceptions as errors


def format_date(date: Union[str, datetime, None]) -> Union[str, None]:
    """Convert date to the format required by PostMark."""
    if date is None:
        return None

    if type(date) is str:
        date_parsed = parse(date, settings={"STRICT_PARSING": True})
        if date_parsed is None:
            raise ValueError(f"Could not parse the date: {date}")
    elif type(date) is datetime:
        date_parsed = date
    return date_parsed.strftime(r"%Y-%m-%d")


class ResponseTuple(NamedTuple):
    """Container for bundling response status code and json content."""

    status_code: int
    json: dict


class PostDmarc:
    """Connection object to the Postmark DMARC API."""

    def __init__(self) -> None:
        """Initialize object with default values."""
        self.api_key = self.get_api_key()
        self.endpoint = "https://dmarc.postmarkapp.com"
        self.session = requests.Session()
        self.session.headers.update(
            {"X-Api-Token": self.api_key, "Accept": "application/json"}
        )

    def get_api_key(self) -> str:
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
                    PM_API_KEY = f.read().strip()
            except FileNotFoundError:
                raise errors.APIKeyMissingError(
                    f"All methods require an API key. Please set the API key in either "
                    f"the 'POSTMARK_API_KEY' environment variable or in "
                    f"the {path} file."
                )
        return PM_API_KEY

    def check_response(self, response: requests.Response) -> None:
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
        mapping: DefaultDict[int, Optional[Type[Exception]]] = defaultdict(
            Type[errors.UnrecognizedStatusCodeError]
        )
        mapping.update(
            [
                (200, None),
                (204, None),
                (303, None),
                (400, errors.BadRequestError),
                (404, errors.PageNotFoundError),
                (422, errors.UnprocessableEntityError),
                (500, errors.InternalServerError),
            ]
        )

        mapped_status_code = mapping[response.status_code]

        if mapped_status_code is not None:
            raise mapped_status_code(response.json()["message"])
        else:
            return None

    def create_record(self, email: str, domain: str) -> ResponseTuple:
        """Create a new DMARC record for a given domain and email."""
        endpoint_path = "/records"
        body = {"email": email, "domain": domain}
        del self.session.headers["X-Api-Token"]
        response = self.session.post(self.endpoint + endpoint_path, json=body)
        self.session.headers.update({"X-Api-Token": self.api_key})
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def get_record(self) -> ResponseTuple:
        """Get a record’s information."""
        endpoint_path = "/records/my"
        response = self.session.get(self.endpoint + endpoint_path)
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def update_record(self, email: str) -> ResponseTuple:
        """Update a record’s information."""
        self.session.headers.update({"Content-Type": "application/json"})
        endpoint_path = "/records/patch"
        body = {"email": email}
        response = self.session.patch(self.endpoint + endpoint_path, json=body)
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def get_dns_snippet(self) -> ResponseTuple:
        """Get generated DMARC DNS record name and value."""
        endpoint_path = "/records/my/dns"
        response = self.session.get(self.endpoint + endpoint_path)
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def verify_dns(self) -> ResponseTuple:
        """Verify if your DMARC DNS record exists."""
        endpoint_path = "/records/my/verify"
        response = self.session.post(self.endpoint + endpoint_path)
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def delete_record(self) -> ResponseTuple:
        """Delete a record.

        Deleting a record will stop processing data for this domain.
        The email associated with this record will also be unsubscribed from the DMARC
        weekly digests for this domain only.
        """
        endpoint_path = "/records/my"
        response = self.session.delete(self.endpoint + endpoint_path)
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def list_reports(
        self,
        from_date: Union[str, datetime, None] = None,
        to_date: Union[str, datetime, None] = None,
        limit: int = None,
        after: int = None,
        before: int = None,
        reverse: bool = None,
    ) -> ResponseTuple:
        """List all received DMARC reports for a given domain.

        List all received DMARC reports for a given domain with the ability to filter
        results by a single date or date range.

        Keyword Arguments:
        from_date   Only include reports received on this date or after.
        to_date     Only include reports received before this date.
        limit       Limit the number of returned reports to the specified value.
                        (default 30, max 50)
        after       Only include reports with IDs higher than the specified value.
                        Used for pagination.
        before      Only include reports with IDs lower than the specified value.
                        Used for pagination.
        reverse     Set to true to list reports in reverse order (default false)
        """
        endpoint_path = "/records/my/reports"
        params = {
            "from_date": format_date(from_date),
            "to_date": format_date(to_date),
            "limit": limit,
            "after": after,
            "before": before,
            "reverse": reverse,
        }

        params = {key: value for key, value in params.items() if value is not None}

        response = self.session.get(self.endpoint + endpoint_path, params=params)
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def get_report(self, id: int, fmt: str = "json") -> ResponseTuple:
        """Load full DMARC report details.

        Load full DMARC report details as a raw DMARC XML document
        or as our own JSON representation.
        """
        if fmt == "json":
            self.session.headers.update({"Content-Type": "application/json"})
        elif fmt == "xml":
            self.session.headers.update({"Content-Type": "application/xml"})
        else:
            raise errors.BadRequestError(
                f"Format keyword must be either 'json' or 'xml', not {fmt}."
            )

        endpoint_path = f"/records/my/reports/{id}"
        response = self.session.get(self.endpoint + endpoint_path)
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def export_all_reports(
        self,
        from_date: Union[str, datetime],
        to_date: Union[str, datetime],
        filepath: str,
    ) -> None:
        """Query for all forensic reports in a date range and export to a json file.

        Arguments:
        from_date   Only include reports received on this date or after.
        to_date     Only include reports received before this date.
        filepath    The file name to export to. Should end in ".json".
        """
        reports = []
        output = []

        params = {
            "from_date": from_date,
            "to_date": to_date,
            "after": None,
        }
        # Get first batch of reports
        current_reports = self.list_reports(**params)
        params["after"] = current_reports["meta"]["next"]
        reports.extend(current_reports["entries"])

        # Get any subsequent reports
        while params["after"] is not None:
            current_reports = self.list_reports(**params)
            params["after"] = current_reports["meta"]["next"]
            reports.extend(current_reports["entries"])

        ids = [entry["id"] for entry in reports]
        output.extend([self.get_report(ident) for ident in ids])

        with open(filepath, "w") as f:
            json.dump(output, f)

    def recover_token(self, owner: str) -> ResponseTuple:
        """Initiate API token recovery for a domain.

        This endpoint is public and doesn't require authentication.
        """
        self.session.headers.update({"Content-Type": "application/json"})
        endpoint_path = "/tokens/recover"
        body = {"owner": owner}
        del self.session.headers["X-Api-Token"]
        response = self.session.post(self.endpoint + endpoint_path, json=body)
        self.session.headers.update({"X-Api-Token": self.api_key})
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())

    def rotate_token(self) -> ResponseTuple:
        """Generate a new API token and replace your existing one with it."""
        # TODO: Think about how to implement key rotation within this wrapper
        endpoint_path = "/records/my/token/rotate"
        response = self.session.post(self.endpoint + endpoint_path)
        self.check_response(response)
        return ResponseTuple(response.status_code, response.json())


def main() -> None:
    """Run default behavior: retrieve forensic reports from the past 7 days."""
    fire.Fire(PostDmarc)


if __name__ == "__main__":
    main()
