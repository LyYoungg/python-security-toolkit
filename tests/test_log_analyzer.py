from log_analyzer.log_analyzer import (
    analyze_events,
    load_events,
    parse_log_line,
    validate_log_file,
)


def test_parse_failed_login():
    line = (
        "2026-08-22 09:04:01 FAILED_LOGIN "
        "user=admin ip=192.168.10.45"
    )

    event = parse_log_line(line)

    assert event is not None
    assert event["event"] == "FAILED_LOGIN"
    assert event["user"] == "admin"
    assert event["ip"] == "192.168.10.45"


def test_reject_invalid_log_line():
    assert parse_log_line("invalid log entry") is None


def test_reject_invalid_ip():
    line = (
        "2026-08-22 09:04:01 FAILED_LOGIN "
        "user=admin ip=999.168.10.45"
    )

    assert parse_log_line(line) is None


def test_analyze_failed_logins():
    events = [
        {
            "timestamp": "2026-08-22 09:00:00",
            "event": "FAILED_LOGIN",
            "user": "admin",
            "ip": "192.168.10.45",
        },
        {
            "timestamp": "2026-08-22 09:00:01",
            "event": "FAILED_LOGIN",
            "user": "admin",
            "ip": "192.168.10.45",
        },
    ]

    results = analyze_events(events, failure_threshold=2)

    assert results["failed_logins"] == 2
    assert len(results["alerts"]) == 1
    assert results["alerts"][0]["ip"] == "192.168.10.45"


def test_below_threshold_does_not_alert():
    events = [
        {
            "timestamp": "2026-08-22 09:00:00",
            "event": "FAILED_LOGIN",
            "user": "admin",
            "ip": "192.168.10.45",
        }
    ]

    results = analyze_events(events, failure_threshold=5)

    assert results["alerts"] == []


def test_load_events_tracks_invalid_lines(tmp_path):
    log_file = tmp_path / "auth.log"

    log_file.write_text(
        "2026-08-22 09:00:00 SUCCESS_LOGIN "
        "user=jsmith ip=192.168.10.21\n"
        "BROKEN LOG ENTRY\n",
        encoding="utf-8",
    )

    events, invalid_lines = load_events(log_file)

    assert len(events) == 1
    assert invalid_lines == [2]


def test_missing_log_file(tmp_path):
    missing_file = tmp_path / "missing.log"

    try:
        validate_log_file(missing_file)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Expected FileNotFoundError")