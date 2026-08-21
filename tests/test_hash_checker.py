import hashlib

import pytest

from hash_checker.hash_checker import calculate_sha256


def test_calculate_sha256(tmp_path):
    test_file = tmp_path / "example.txt"
    test_file.write_text("Python Security Toolkit", encoding="utf-8")

    expected_hash = hashlib.sha256(
        b"Python Security Toolkit"
    ).hexdigest()

    actual_hash = calculate_sha256(test_file)

    assert actual_hash == expected_hash


def test_missing_file_raises_error(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        calculate_sha256(missing_file)


def test_directory_raises_value_error(tmp_path):
    with pytest.raises(ValueError):
        calculate_sha256(tmp_path)