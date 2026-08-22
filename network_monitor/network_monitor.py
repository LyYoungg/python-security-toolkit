import socket

import psutil

def format_bytes(value):
    """Convert a byte count into a readable unit."""

    units = (
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    )

    size = float(value)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"

def get_system_identity():
    """Return basic local network identity information."""

    hostname = socket.gethostname()

    try:
        primary_ip = socket.gethostbyname(
            hostname
        )
    except socket.gaierror:
        primary_ip = "Unavailable"

    return {
        "hostname": hostname,
        "primary_ip": primary_ip,
    }

def get_interface_information():
    """Collect network interface status and addresses."""

    addresses = psutil.net_if_addrs()
    statistics = psutil.net_if_stats()

    interfaces = []

    for interface_name in sorted(addresses):
        interface_data = {
            "name": interface_name,
            "is_up": False,
            "speed_mbps": 0,
            "ipv4": [],
            "ipv6": [],
        }

        if interface_name in statistics:
            interface_data["is_up"] = statistics[
                interface_name
            ].isup

            interface_data["speed_mbps"] = statistics[
                interface_name
            ].speed

        for address in addresses[interface_name]:
            if address.family == socket.AF_INET:
                interface_data["ipv4"].append(
                    address.address
                )

            elif address.family == socket.AF_INET6:
                clean_ipv6 = address.address.split("%")[0]

                interface_data["ipv6"].append(
                    clean_ipv6
                )

        interfaces.append(interface_data)

    return interfaces

def get_traffic_statistics():
    """Return system-wide network traffic counters."""

    counters = psutil.net_io_counters()

    return {
        "bytes_sent": counters.bytes_sent,
        "bytes_received": counters.bytes_recv,
        "packets_sent": counters.packets_sent,
        "packets_received": counters.packets_recv,
        "errors_in": counters.errin,
        "errors_out": counters.errout,
        "drops_in": counters.dropin,
        "drops_out": counters.dropout,
    }

def print_system_summary(identity):
    """Display local network identity."""

    print("\nSystem Network Identity")
    print("-" * 60)

    print(
        f"Hostname:   {identity['hostname']}"
    )

    print(
        f"Primary IP: {identity['primary_ip']}"
    )

def print_interfaces(interfaces):
    """Display local network interface information."""

    print("\nNetwork Interfaces")
    print("-" * 60)

    for interface in interfaces:
        status = (
            "UP"
            if interface["is_up"]
            else "DOWN"
        )

        print(
            f"\nInterface: {interface['name']}"
        )

        print(
            f"Status:    {status}"
        )

        if interface["speed_mbps"] > 0:
            print(
                f"Speed:     "
                f"{interface['speed_mbps']} Mbps"
            )
        else:
            print("Speed:     Unknown")

        if interface["ipv4"]:
            for address in interface["ipv4"]:
                print(f"IPv4:      {address}")
        else:
            print("IPv4:      None")

        if interface["ipv6"]:
            for address in interface["ipv6"]:
                print(f"IPv6:      {address}")

def print_traffic_statistics(statistics):
    """Display local network traffic statistics."""

    print("\nNetwork Traffic")
    print("-" * 60)

    print(
        "Data sent:        "
        f"{format_bytes(statistics['bytes_sent'])}"
    )

    print(
        "Data received:    "
        f"{format_bytes(statistics['bytes_received'])}"
    )

    print(
        "Packets sent:     "
        f"{statistics['packets_sent']}"
    )

    print(
        "Packets received: "
        f"{statistics['packets_received']}"
    )

    print(
        "Receive errors:   "
        f"{statistics['errors_in']}"
    )

    print(
        "Send errors:      "
        f"{statistics['errors_out']}"
    )

    print(
        "Receive drops:    "
        f"{statistics['drops_in']}"
    )

    print(
        "Send drops:       "
        f"{statistics['drops_out']}"
    )

def main():
    """Run the local Network Monitor."""

    print("=" * 60)
    print("LOCAL NETWORK MONITOR")
    print("=" * 60)

    print(
        "\nCollecting local interface and "
        "traffic information..."
    )

    try:
        identity = get_system_identity()
        interfaces = get_interface_information()
        traffic = get_traffic_statistics()

        print_system_summary(identity)
        print_interfaces(interfaces)
        print_traffic_statistics(traffic)

    except PermissionError:
        print(
            "\n[ERROR] Permission denied while "
            "reading network information."
        )

    except OSError as error:
        print(
            f"\n[ERROR] Unable to collect network "
            f"information: {error}"
        )


if __name__ == "__main__":
    main()