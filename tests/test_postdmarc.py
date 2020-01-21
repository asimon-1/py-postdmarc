import unittest
import os
from unittest.mock import patch
import postdmarc.postdmarc as pdm
from postdmarc.pdm_exceptions import APIKeyMissingError


class TestResponse(unittest.TestCase):
    def setUp(self):
        self.connection = pdm.PostDmarc()

    def tearDown(self):
        pass

    def test_naiive_test(self):
        pass

    @patch.object(pdm.requests.Session, "post")
    def test_create_record(self, mock_post):
        mock_post.return_value.json.return_value = {
            "domain": "postmarkapp.com",
            "public_token": "1mVgKNr5scA",
            "created_at": "2014-06-25T19:22:53Z",
            "private_token": "005d8431-b020-41aa-230e-4d63a0357869",
            "reporting_uri": "mailto:randomhash+1mSgANr7scM@inbound.postmarkapp.com",
            "email": "tema@wildbit.com",
        }
        response = self.connection.create_record("tema@wildbit.com", "postmarkapp.com")

        for response_key in (
            "domain",
            "public_token",
            "created_at",
            "private_token",
            "reporting_uri",
            "email",
        ):
            with self.subTest(response_key=response_key):
                self.assertIn(response_key, response)


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
        connection = pdm.PostDmarc()
        self.assertIn("X-Api-Token", connection.session.headers)
        self.assertEqual("testvalue", connection.session.headers["X-Api-Token"])

    @patch.dict("os.environ", {}, clear=True)
    def test_load_api_key_file(self):
        """Ensure that the API key is loaded from a file correctly."""
        with open(self.path, "w") as f:
            f.write("testvalue-file")
        connection = pdm.PostDmarc()
        self.assertIn("X-Api-Token", connection.session.headers)
        self.assertEqual("testvalue-file", connection.session.headers["X-Api-Token"])

    @patch.dict("os.environ", {}, clear=True)
    def test_api_key_not_found(self):
        """Ensure that a missing API key raises an error."""
        self.assertRaises(APIKeyMissingError, pdm.PostDmarc)
