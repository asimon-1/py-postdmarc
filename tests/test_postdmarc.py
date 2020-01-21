import unittest
import os
from unittest.mock import patch
import postdmarc.postdmarc as pdm
from postdmarc.pm_exceptions import APIKeyMissingError


class TestResponse(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_naiive_test(self):
        pass


class TestAPIKey(unittest.TestCase):
    """Test that the API key is set correctly."""

    def setUp(self):
        """Store the real API key in a temporary file, if it exists."""
        self.path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "PM_API.key"
        )
        self.tmp_path = f"{self.path}.tmp"

        # Delete previous temporary file
        if os.path.exists(self.tmp_path):
            os.remove(self.tmp_path)

        # Rename real API key file
        if os.path.exists(self.path):
            os.rename(self.path, self.tmp_path)

    def tearDown(self):
        """Restore the real API key from the temporary file, if it exists."""
        # Delete the test API key file
        if os.path.exists(self.path):
            os.remove(self.path)

        # Restore the real API key file
        if os.path.exists(self.tmp_path):
            os.rename(self.tmp_path, self.path)

    @patch.dict("os.environ", {"POSTMARK_API_KEY": "testvalue"})
    def test_load_api_key_env(self):
        """Ensure the API key is loaded from environment variables correctly."""
        self.assertIn("POSTMARK_API_KEY", os.environ)
        session = pdm.setup()
        self.assertIn("X-Api-Token", session.headers)
        self.assertEqual("testvalue", session.headers["X-Api-Token"])

    @patch.dict("os.environ", {}, clear=True)
    def test_load_api_key_file(self):
        """Ensure that the API key is loaded from a file correctly."""
        with open(self.path, "w") as f:
            f.write("testvalue-file")
        session = pdm.setup()
        self.assertIn("X-Api-Token", session.headers)
        self.assertEqual("testvalue-file", session.headers["X-Api-Token"])

    @patch.dict("os.environ", {}, clear=True)
    def test_api_key_not_found(self):
        """Ensure that a missing API key raises an error."""
        self.assertRaises(APIKeyMissingError, pdm.setup)
