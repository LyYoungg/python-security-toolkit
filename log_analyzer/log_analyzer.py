import re
from collections import Counter, defaultdict
from pathlib import Path
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<event>SUCCESS_LOGIN|FAILED_LOGIN) "
    r"user=(?P<user>[A-Za-z0-9_.-]+) "
    r"ip=(?P<ip>\d{1,3}(?:\.\d{1,3}){3})$"
)

DEFAULT_FAILURE_THRESHOLD = 5

def validate_log_file(log_file):
    """Validate that the supplied log path exists and is a file."""

    path = Path(log_file)

    if not path.exists():
        raise FileNotFoundError(f"Log file does not exist: {path}")

    if not path.is_file():
        raise ValueError(f"Log path is not a file: {path}")

    return path
def parse_log_line(line):
    """Parse one authentication log entry."""

    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    event = match.groupdict()

    octets = event["ip"].split(".")

    if any(int(octet) > 255 for octet in octets):
        return None

    return event
{
    "timestamp": "2026-08-22 09:14:21",
    "event": "FAILED_LOGIN",
    "user": "admin",
    "ip": "192.168.10.45",
}
def load_events(log_file):
    """Load valid authentication events from a log file."""

    log_path = validate_log_file(log_file)

    events = []
    invalid_lines = []

    with log_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            event = parse_log_line(line)

            if event is None:
                invalid_lines.append(line_number)
            else:
                events.append(event)

    return events, invalid_lines
def analyze_events(events, failure_threshold=DEFAULT_FAILURE_THRESHOLD):
    """Analyze authentication events for repeated failures."""

    successful_logins = 0
    failed_logins = 0

    failures_by_ip = Counter()
    targeted_users = defaultdict(set)

    for event in events:
        if event["event"] == "SUCCESS_LOGIN":
            successful_logins += 1

        elif event["event"] == "FAILED_LOGIN":
            failed_logins += 1
            failures_by_ip[event["ip"]] += 1
            targeted_users[event["ip"]].add(event["user"])

    alerts = []

    for ip, failure_count in failures_by_ip.items():
        if failure_count >= failure_threshold:
            alerts.append(
                {
                    "ip": ip,
                    "failures": failure_count,
                    "users": sorted(targeted_users[ip]),
                }
            )

    alerts.sort(
        key=lambda alert: alert["failures"],
        reverse=True,
    )

    return {
        "total_events": len(events),
        "successful_logins": successful_logins,
        "failed_logins": failed_logins,
        "failures_by_ip": dict(failures_by_ip),
        "alerts": alerts,
    }

def print_report(results, invalid_lines):
    """Display the authentication log analysis."""

    print("\n" + "=" * 60)
    print("SECURITY LOG ANALYSIS")
    print("=" * 60)

    print(f"Total valid events:     {results['total_events']}")
    print(f"Successful logins:      {results['successful_logins']}")
    print(f"Failed logins:          {results['failed_logins']}")
    print(f"Invalid log entries:    {len(invalid_lines)}")

    print("\nFailed Authentication Sources")
    print("-" * 60)

    if results["failures_by_ip"]:
        for ip, count in sorted(
            results["failures_by_ip"].items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            print(f"{ip:<20} {count} failure(s)")
    else:
        print("No failed authentication events detected.")

    print("\nDetection Alerts")
    print("-" * 60)

    if results["alerts"]:
        for alert in results["alerts"]:
            users = ", ".join(alert["users"])

            print(f"[ALERT] Source IP: {alert['ip']}")
            print(f"        Failed logins: {alert['failures']}")
            print(f"        Targeted users: {users}")
    else:
        print("No sources exceeded the configured threshold.")

    if invalid_lines:
        line_list = ", ".join(str(number) for number in invalid_lines)

        print("\nParser Warnings")
        print("-" * 60)
        print(f"[WARNING] Invalid entries on line(s): {line_list}")

def main():
    """Run the Security Log Analyzer."""

    print("=" * 60)
    print("SECURITY LOG ANALYZER")
    print("=" * 60)

    log_file = input("\nAuthentication log file: ").strip()

    threshold_input = input(
        f"Failed-login alert threshold "
        f"[{DEFAULT_FAILURE_THRESHOLD}]: "
    ).strip()

    try:
        if threshold_input:
            threshold = int(threshold_input)

            if threshold < 1:
                raise ValueError(
                    "Alert threshold must be at least 1."
                )
        else:
            threshold = DEFAULT_FAILURE_THRESHOLD

        events, invalid_lines = load_events(log_file)

        results = analyze_events(
            events,
            failure_threshold=threshold,
        )

        print_report(results, invalid_lines)

    except FileNotFoundError as error:
        print(f"\n[ERROR] {error}")

    except ValueError as error:
        print(f"\n[ERROR] {error}")

    except PermissionError:
        print("\n[ERROR] Permission denied while reading log file.")

    except OSError as error:
        print(f"\n[ERROR] Unable to process log file: {error}")


if __name__ == "__main__":
    main()