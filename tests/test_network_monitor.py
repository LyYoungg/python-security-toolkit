from network_monitor.network_monitor import (
    format_bytes,
    get_interface_information,
    get_system_identity,
    get_traffic_statistics,
)


def test_format_bytes():
    assert format_bytes(0) == "0.00 B"
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1048576) == "1.00 MB"


def test_system_identity_structure():
    identity = get_system_identity()

    assert "hostname" in identity
    assert "primary_ip" in identity
    assert identity["hostname"]


def test_interface_information_structure():
    interfaces = get_interface_information()

    assert isinstance(interfaces, list)

    for interface in interfaces:
        assert "name" in interface
        assert "is_up" in interface
        assert "speed_mbps" in interface
        assert "ipv4" in interface
        assert "ipv6" in interface


def test_traffic_statistics_structure():
    statistics = get_traffic_statistics()

    expected_keys = {
        "bytes_sent",
        "bytes_received",
        "packets_sent",
        "packets_received",
        "errors_in",
        "errors_out",
        "drops_in",
        "drops_out",
    }

    assert expected_keys.issubset(
        statistics.keys()
    )


def test_network_counters_nonnegative():
    statistics = get_traffic_statistics()

    assert statistics["bytes_sent"] >= 0
    assert statistics["bytes_received"] >= 0
    assert statistics["packets_sent"] >= 0
    assert statistics["packets_received"] >= 0

    