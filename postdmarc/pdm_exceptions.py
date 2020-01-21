"""Custom exception types for the Postmark DMARC API."""


class APIKeyMissingError(Exception):
    """Could not find the API key."""

    pass


class BadRequestError(Exception):
    """Something with your request isn’t quite right, this could be malformed JSON."""

    pass


class PageNotFoundError(Exception):
    """The requested URI could not be found."""

    pass


class UnprocessableEntityError(Exception):
    """Your request has failed validations."""

    pass


class InternalServerError(Exception):
    """Our servers have failed to process your request."""

    pass


class UnrecognizedStatusCodeError(Exception):
    """The server returned an unknown status code."""

    pass
