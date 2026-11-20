import unittest

from code_examples.modernized.stdlib_usage_modernized import (
    is_supported_version,
    validate_payload,
)


class StdlibUsageModernizedTests(unittest.TestCase):
    def test_supported_version_true_for_newer_version(self):
        self.assertTrue(is_supported_version("1.3.0"))

    def test_supported_version_false_for_older_version(self):
        self.assertFalse(is_supported_version("1.1.0"))

    def test_validate_payload_accepts_mapping(self):
        self.assertTrue(validate_payload({"key": "value"}))

    def test_validate_payload_rejects_non_mapping(self):
        with self.assertRaises(TypeError):
            validate_payload(["not", "a", "mapping"])


if __name__ == "__main__":
    unittest.main()
