import hashlib
from pathlib import Path



def calculate_sha256(file_path):
    """Calculate and return the SHA-256 hash of a file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    sha256 = hashlib.sha256()

    with path.open("rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()
def main():
    print("=" * 60)
    print("SHA-256 HASH CHECKER")
    print("=" * 60)

    file_path = input("Enter the path of the file to hash: ").strip()

    try:
        digest = calculate_sha256(file_path)

        print("\nHash calculated successfully.")
        print(f"\nFile:   {file_path}")
        print(f"SHA-256: {digest}")

    except FileNotFoundError as error:
        print(f"\n[ERROR] {error}")

    except PermissionError:
        print("\n[ERROR] Permission denied while reading the file.")

    except ValueError as error:
        print(f"\n[ERROR] {error}")

    except OSError as error:
        print(f"\n[ERROR] Unable to process file: {error}")


if __name__ == "__main__":
    main()