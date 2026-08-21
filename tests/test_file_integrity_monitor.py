import json

import pytest

from file_integrity_monitor.file_integrity_monitor import (
    compare_baseline,
    create_baseline,
    hash_directory,
    load_baseline,
    validate_directory,
)

def test_hash_directory(tmp_path):
    file_one = tmp_path / "one.txt"
    file_two = tmp_path / "two.txt"

    file_one.write_text("File One", encoding="utf-8")
    file_two.write_text("File Two", encoding="utf-8")

    hashes = hash_directory(tmp_path)

    assert "one.txt" in hashes
    assert "two.txt" in hashes
    assert len(hashes) == 2

def test_create_baseline(tmp_path):
    monitored_directory = tmp_path / "monitored"
    monitored_directory.mkdir()

    test_file = monitored_directory / "example.txt"
    test_file.write_text(
        "Known good content",
        encoding="utf-8",
    )

    baseline_file = tmp_path / "baseline.json"

    file_count = create_baseline(
        monitored_directory,
        baseline_file,
    )

    assert file_count == 1
    assert baseline_file.exists()

    baseline = load_baseline(baseline_file)

    assert baseline["algorithm"] == "SHA-256"
    assert "example.txt" in baseline["files"]

def test_detect_modified_file(tmp_path):
    monitored_directory = tmp_path / "monitored"
    monitored_directory.mkdir()

    test_file = monitored_directory / "config.txt"
    test_file.write_text(
        "secure=true",
        encoding="utf-8",
    )

    baseline_file = tmp_path / "baseline.json"

    create_baseline(
        monitored_directory,
        baseline_file,
    )

    test_file.write_text(
        "secure=false",
        encoding="utf-8",
    )

    results = compare_baseline(
        monitored_directory,
        baseline_file,
    )

    assert "config.txt" in results["modified"]

def test_detect_new_file(tmp_path):
    monitored_directory = tmp_path / "monitored"
    monitored_directory.mkdir()

    original_file = monitored_directory / "original.txt"
    original_file.write_text(
        "Original",
        encoding="utf-8",
    )

    baseline_file = tmp_path / "baseline.json"

    create_baseline(
        monitored_directory,
        baseline_file,
    )

    new_file = monitored_directory / "new.txt"
    new_file.write_text(
        "New file",
        encoding="utf-8",
    )

    results = compare_baseline(
        monitored_directory,
        baseline_file,
    )

    assert "new.txt" in results["new"]

def test_detect_deleted_file(tmp_path):
    monitored_directory = tmp_path / "monitored"
    monitored_directory.mkdir()

    test_file = monitored_directory / "delete_me.txt"
    test_file.write_text(
        "Temporary",
        encoding="utf-8",
    )

    baseline_file = tmp_path / "baseline.json"

    create_baseline(
        monitored_directory,
        baseline_file,
    )

    test_file.unlink()

    results = compare_baseline(
        monitored_directory,
        baseline_file,
    )

    assert "delete_me.txt" in results["deleted"]

def test_missing_directory_raises_error(tmp_path):
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileNotFoundError):
        validate_directory(missing_directory)


def test_file_rejected_as_directory(tmp_path):
    test_file = tmp_path / "file.txt"
    test_file.write_text(
        "Not a directory",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        validate_directory(test_file)

def test_invalid_baseline_json(tmp_path):
    baseline_file = tmp_path / "baseline.json"

    baseline_file.write_text(
        "{ definitely not valid json",
        encoding="utf-8",
    )

    with pytest.raises(json.JSONDecodeError):
        load_baseline(baseline_file)