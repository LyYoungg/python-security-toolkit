import pytest

from port_scanner.port_scanner import (
    scan_port,
    validate_port_range,
    validate_target,
)


def test_localhost_is_allowed():
    assert validate_target("localhost") == "127.0.0.1"


def test_loopback_is_allowed():
    assert validate_target("127.0.0.1") == "127.0.0.1"


def test_private_address_is_allowed():
    assert validate_target("192.168.1.10") == "192.168.1.10"


def test_public_address_is_blocked():
    with pytest.raises(ValueError):
        validate_target("8.8.8.8")


def test_invalid_target_is_blocked():
    with pytest.raises(ValueError):
        validate_target("definitely-not-an-ip")


def test_valid_port_range():
    start, end = validate_port_range(
        20,
        100,
    )

    assert start == 20
    assert end == 100


def test_reversed_port_range_rejected():
    with pytest.raises(ValueError):
        validate_port_range(
            100,
            20,
        )


def test_excessive_port_range_rejected():
    with pytest.raises(ValueError):
        validate_port_range(
            1,
            5000,
        )


def test_closed_local_port_returns_boolean():
    result = scan_port(
        "127.0.0.1",
        65534,
        timeout=0.1,
    )

    assert isinstance(result, bool)
