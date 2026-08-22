from file_integrity_monitor.file_integrity_monitor import (
    main as file_integrity_main,
)
from hash_checker.hash_checker import main as hash_checker_main
from log_analyzer.log_analyzer import main as log_analyzer_main
from network_monitor.network_monitor import main as network_monitor_main
from password_auditor.password_auditor import main as password_auditor_main
from port_scanner.port_scanner import main as port_scanner_main

def print_banner():
    """Display the toolkit banner and main menu."""

    print("\n" + "=" * 60)
    print("                 PYTHON SECURITY TOOLKIT")
    print("=" * 60)

    print("\nDefensive Security & System Analysis Utilities")

    print("\n[1] SHA-256 Hash Checker")
    print("[2] File Integrity Monitor")
    print("[3] Security Log Analyzer")
    print("[4] Password Auditor")
    print("[5] Authorized Port Scanner")
    print("[6] Local Network Monitor")

    print("\n[0] Exit")
def wait_for_return():
    """Pause before returning to the main menu."""

    input("\nPress Enter to return to the main menu...")
def run_tool(choice):
    """Run the selected toolkit component."""

    tools = {
        "1": hash_checker_main,
        "2": file_integrity_main,
        "3": log_analyzer_main,
        "4": password_auditor_main,
        "5": port_scanner_main,
        "6": network_monitor_main,
    }

    selected_tool = tools.get(choice)

    if selected_tool is None:
        return False

    print()
    selected_tool()

    return True

def main():
    """Run the unified Python Security Toolkit interface."""

    while True:
        print_banner()

        choice = input("\nSelect an option: ").strip()

        if choice == "0":
            print("\nExiting Python Security Toolkit.")
            print("Goodbye.\n")
            break

        if run_tool(choice):
            wait_for_return()
        else:
            print(
                "\n[ERROR] Invalid selection. "
                "Choose an option from 0 through 6."
            )

            wait_for_return()


if __name__ == "__main__":
    main()
    