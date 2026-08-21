import json
from pathlib import Path

from hash_checker.hash_checker import calculate_sha256


def validate_directory(directory):
    """Validate that a supplied path exists and is a directory."""

    path = Path(directory)

    if not path.exists():
        raise FileNotFoundError(f"Directory does not exist: {path}")

    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")

    return path

def hash_directory(directory):
    """Calculate SHA-256 hashes for all files in a directory."""

    directory = validate_directory(directory)

    hashes = {}

    for path in sorted(directory.rglob("*")):
        if path.is_file():
            relative_path = path.relative_to(directory).as_posix()
            hashes[relative_path] = calculate_sha256(path)

    return hashes

def create_baseline(directory, baseline_file):
    """Create a JSON baseline containing hashes for a directory."""

    hashes = hash_directory(directory)

    baseline_path = Path(baseline_file)

    baseline_data = {
        "algorithm": "SHA-256",
        "directory": str(Path(directory)),
        "files": hashes,
    }

    with baseline_path.open("w", encoding="utf-8") as file:
        json.dump(baseline_data, file, indent=4)

    return len(hashes)
def load_baseline(baseline_file):
    """Load and validate an existing JSON baseline."""

    baseline_path = Path(baseline_file)

    if not baseline_path.exists():
        raise FileNotFoundError(
            f"Baseline file does not exist: {baseline_path}"
        )

    if not baseline_path.is_file():
        raise ValueError(
            f"Baseline path is not a file: {baseline_path}"
        )

    with baseline_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if "files" not in data:
        raise ValueError("Invalid baseline: missing 'files' data.")

    return data
def compare_baseline(directory, baseline_file):
    """Compare current directory hashes against a saved baseline."""

    baseline = load_baseline(baseline_file)

    old_hashes = baseline["files"]
    current_hashes = hash_directory(directory)

    unchanged = []
    modified = []
    new = []
    deleted = []

    for file_path, current_hash in current_hashes.items():
        if file_path not in old_hashes:
            new.append(file_path)

        elif current_hash != old_hashes[file_path]:
            modified.append(file_path)

        else:
            unchanged.append(file_path)

    for file_path in old_hashes:
        if file_path not in current_hashes:
            deleted.append(file_path)

    return {
        "unchanged": sorted(unchanged),
        "modified": sorted(modified),
        "new": sorted(new),
        "deleted": sorted(deleted),
    }

def print_report(results):
    """Display file integrity comparison results."""

    print("\n" + "=" * 60)
    print("FILE INTEGRITY REPORT")
    print("=" * 60)

    for file_path in results["unchanged"]:
        print(f"[OK]       {file_path}")

    for file_path in results["modified"]:
        print(f"[MODIFIED] {file_path}")

    for file_path in results["new"]:
        print(f"[NEW]      {file_path}")

    for file_path in results["deleted"]:
        print(f"[DELETED]  {file_path}")

    print("\nSummary")
    print("-" * 60)
    print(f"Unchanged: {len(results['unchanged'])}")
    print(f"Modified:  {len(results['modified'])}")
    print(f"New:       {len(results['new'])}")
    print(f"Deleted:   {len(results['deleted'])}")

def main():
    print("=" * 60)
    print("FILE INTEGRITY MONITOR")
    print("=" * 60)

    print("\n[1] Create baseline")
    print("[2] Verify directory")
    print("[0] Exit")

    choice = input("\nSelect an option: ").strip()

    try:
        if choice == "1":
            directory = input(
                "Directory to monitor: "
            ).strip()

            baseline_file = input(
                "Baseline filename [baseline.json]: "
            ).strip()

            if not baseline_file:
                baseline_file = "baseline.json"

            file_count = create_baseline(
                directory,
                baseline_file,
            )

            print(
                f"\n[OK] Baseline created successfully "
                f"for {file_count} file(s)."
            )

            print(
                f"Baseline saved to: {baseline_file}"
            )

        elif choice == "2":
            directory = input(
                "Directory to verify: "
            ).strip()

            baseline_file = input(
                "Baseline filename [baseline.json]: "
            ).strip()

            if not baseline_file:
                baseline_file = "baseline.json"

            results = compare_baseline(
                directory,
                baseline_file,
            )

            print_report(results)

        elif choice == "0":
            print("\nExiting File Integrity Monitor.")

        else:
            print("\n[ERROR] Invalid menu selection.")

    except FileNotFoundError as error:
        print(f"\n[ERROR] {error}")

    except PermissionError:
        print(
            "\n[ERROR] Permission denied while "
            "accessing a file."
        )

    except json.JSONDecodeError:
        print(
            "\n[ERROR] Baseline file contains "
            "invalid JSON."
        )

    except ValueError as error:
        print(f"\n[ERROR] {error}")

    except OSError as error:
        print(f"\n[ERROR] File operation failed: {error}")


if __name__ == "__main__":
    main()   