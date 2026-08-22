import ipaddress
import socket

DEFAULT_TIMEOUT = 0.5
MAX_PORT_RANGE = 1024

def validate_target(target):
    """Allow only localhost, loopback, or private IPv4 targets."""

    target = target.strip().lower()

    if target == "localhost":
        return "127.0.0.1"

    try:
        address = ipaddress.ip_address(target)
    except ValueError as error:
        raise ValueError(
            "Target must be localhost or a valid IP address."
        ) from error

    if address.version != 4:
        raise ValueError(
            "This educational scanner currently supports IPv4 only."
        )

    if not (address.is_private or address.is_loopback):
        raise ValueError(
            "Public IP addresses are blocked. "
            "Use localhost or an authorized private-network target."
        )

    return str(address)

def validate_port_range(start_port, end_port):
    """Validate a TCP port range."""

    if not 1 <= start_port <= 65535:
        raise ValueError(
            "Start port must be between 1 and 65535."
        )

    if not 1 <= end_port <= 65535:
        raise ValueError(
            "End port must be between 1 and 65535."
        )

    if start_port > end_port:
        raise ValueError(
            "Start port cannot be greater than end port."
        )

    port_count = end_port - start_port + 1

    if port_count > MAX_PORT_RANGE:
        raise ValueError(
            f"Port range cannot exceed {MAX_PORT_RANGE} ports."
        )

    return start_port, end_port
def scan_port(target, port, timeout=DEFAULT_TIMEOUT):
    """Return True if a TCP connection succeeds on the target port."""

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    ) as client_socket:

        client_socket.settimeout(timeout)

        result = client_socket.connect_ex(
            (target, port)
        )

    return result == 0

def scan_range(target, start_port, end_port):
    """Scan an authorized target across a validated TCP port range."""

    target = validate_target(target)

    start_port, end_port = validate_port_range(
        start_port,
        end_port,
    )

    results = []

    for port in range(start_port, end_port + 1):
        is_open = scan_port(target, port)

        results.append(
            {
                "port": port,
                "open": is_open,
            }
        )

    return target, results

def print_report(target, results):
    """Display port scan results."""

    print("\n" + "=" * 60)
    print("AUTHORIZED PORT SCAN RESULTS")
    print("=" * 60)

    print(f"\nTarget: {target}")

    print("\nPORT       STATE")
    print("-" * 25)

    for result in results:
        state = "OPEN" if result["open"] else "CLOSED"

        print(
            f"{result['port']:<10} {state}"
        )

    open_ports = [
        result["port"]
        for result in results
        if result["open"]
    ]

    print("\nScan Summary")
    print("-" * 25)
    print(f"Ports scanned: {len(results)}")
    print(f"Open ports:    {len(open_ports)}")

    if open_ports:
        joined_ports = ", ".join(
            str(port)
            for port in open_ports
        )

        print(f"Detected:      {joined_ports}")

def main():
    """Run the Authorized Port Scanner."""

    print("=" * 60)
    print("AUTHORIZED PORT SCANNER")
    print("=" * 60)

    print(
        "\nUse only against localhost, private lab systems, "
        "or systems you are explicitly authorized to test."
    )

    target = input(
        "\nTarget IPv4 address [127.0.0.1]: "
    ).strip()

    if not target:
        target = "127.0.0.1"

    try:
        start_port = int(
            input("Starting port: ").strip()
        )

        end_port = int(
            input("Ending port: ").strip()
        )

        validated_target, results = scan_range(
            target,
            start_port,
            end_port,
        )

        print_report(
            validated_target,
            results,
        )

    except ValueError as error:
        print(f"\n[ERROR] {error}")

    except PermissionError:
        print(
            "\n[ERROR] Permission denied during network operation."
        )

    except OSError as error:
        print(
            f"\n[ERROR] Network operation failed: {error}"
        )


if __name__ == "__main__":
    main()

