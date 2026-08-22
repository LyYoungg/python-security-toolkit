import getpass
import string
import getpass


def audit_password(password):
    # your password checking logic goes here
    pass


def main():
    password = getpass.getpass("Password: ")

    results = audit_password(password)

    # print results here


if __name__ == "__main__":
    main()
getpass.getpass()
COMMON_PASSWORDS = {
    # Extremely common numeric passwords
    "123456",
    "123456789",
    "12345678",
    "12345",
    "1234567",
    "1234567890",
    "111111",
    "000000",
    "123123",
    "121212",
    "654321",
    "7777777",
    "666666",
    "112233",
    "131313",
    "123321",

    # Password variations
    "password",
    "password1",
    "password123",
    "password1234",
    "password01",
    "passw0rd",
    "p@ssword",
    "p@ssw0rd",
    "Password",
    "Password1",
    "Password123",

    # Keyboard patterns
    "qwerty",
    "qwerty123",
    "qwertyuiop",
    "qwerty1",
    "qwerty12",
    "qwerty12345",
    "asdfgh",
    "asdfghjkl",
    "zxcvbnm",
    "1q2w3e4r",
    "1q2w3e4r5t",
    "qazwsx",

    # Common words / phrases
    "admin",
    "admin123",
    "administrator",
    "welcome",
    "welcome1",
    "welcome123",
    "letmein",
    "letmein123",
    "login",
    "login123",
    "guest",
    "guest123",
    "user",
    "user123",
    "master",
    "access",
    "secret",
    "changeme",
    "default",

    # Common names / terms
    "iloveyou",
    "princess",
    "dragon",
    "monkey",
    "football",
    "baseball",
    "soccer",
    "shadow",
    "sunshine",
    "superman",
    "batman",
    "starwars",
    "pokemon",
    "computer",
    "internet",
    "whatever",
    "trustno1",
    "freedom",
    "hello",
    "hello123",

    # Common simple combinations
    "abc123",
    "abcd1234",
    "abc123456",
    "1234abcd",
    "test",
    "test123",
    "testing",
    "root",
    "root123",
    "system",
    "server",
    "security",
    "security1",
    "security123",
}

def contains_sequence(password):
    """Detect simple ascending keyboard/alphanumeric sequences."""

    sequences = (
        "0123456789",
        "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiop",
    )

    lowered = password.lower()

    for sequence in sequences:
        for index in range(len(sequence) - 2):
            fragment = sequence[index:index + 3]

            if fragment in lowered:
                return True

    return False
def contains_repeated_characters(password):
    """Detect three identical consecutive characters."""

    for index in range(len(password) - 2):
        if (
            password[index]
            == password[index + 1]
            == password[index + 2]
        ):
            return True

    return False
def audit_password(password):
    """Evaluate a password against educational security checks."""

    checks = {
        "minimum_length": len(password) >= 12,
        "recommended_length": len(password) >= 16,
        "uppercase": any(
            character.isupper()
            for character in password
        ),
        "lowercase": any(
            character.islower()
            for character in password
        ),
        "digit": any(
            character.isdigit()
            for character in password
        ),
        "symbol": any(
            character in string.punctuation
            for character in password
        ),
        "not_common": password.lower() not in COMMON_PASSWORDS,
        "no_simple_sequence": not contains_sequence(password),
        "no_repeated_characters": not contains_repeated_characters(
            password
        ),
    }

    return checks
def generate_recommendations(checks):
    """Generate recommendations for failed password checks."""

    recommendations = []

    if not checks["minimum_length"]:
        recommendations.append(
            "Use at least 12 characters."
        )

    elif not checks["recommended_length"]:
        recommendations.append(
            "Consider using 16 or more characters."
        )

    if not checks["uppercase"]:
        recommendations.append(
            "Include at least one uppercase letter."
        )

    if not checks["lowercase"]:
        recommendations.append(
            "Include at least one lowercase letter."
        )

    if not checks["digit"]:
        recommendations.append(
            "Include at least one number."
        )

    if not checks["symbol"]:
        recommendations.append(
            "Include at least one symbol."
        )

    if not checks["not_common"]:
        recommendations.append(
            "Avoid commonly used passwords."
        )

    if not checks["no_simple_sequence"]:
        recommendations.append(
            "Avoid predictable sequences."
        )

    if not checks["no_repeated_characters"]:
        recommendations.append(
            "Avoid repeated consecutive characters."
        )

    return recommendations

def determine_result(checks):
    """Determine the overall password audit result."""

    required_checks = (
        "minimum_length",
        "uppercase",
        "lowercase",
        "digit",
        "symbol",
        "not_common",
        "no_simple_sequence",
        "no_repeated_characters",
    )

    if all(checks[check] for check in required_checks):
        if checks["recommended_length"]:
            return "STRONG"

        return "ACCEPTABLE"

    return "NEEDS IMPROVEMENT"

def print_audit(checks, result, recommendations):
    """Display password audit results without displaying the password."""

    labels = {
        "minimum_length": "At least 12 characters",
        "recommended_length": "16+ characters recommended",
        "uppercase": "Contains uppercase letter",
        "lowercase": "Contains lowercase letter",
        "digit": "Contains number",
        "symbol": "Contains symbol",
        "not_common": "Not in common-password list",
        "no_simple_sequence": "No simple sequence detected",
        "no_repeated_characters": "No repeated characters detected",
    }

    print("\n" + "=" * 60)
    print("PASSWORD SECURITY AUDIT")
    print("=" * 60)

    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"

        print(f"[{status:<4}] {labels[check]}")

    print("\nOverall Result")
    print("-" * 60)
    print(result)

    print("\nRecommendations")
    print("-" * 60)

    if recommendations:
        for recommendation in recommendations:
            print(f"- {recommendation}")
    else:
        print("No policy recommendations generated.")

def main():
    """Run the Password Auditor."""

    print("=" * 60)
    print("PASSWORD AUDITOR")
    print("=" * 60)

    print(
        "\nPasswords are evaluated locally and are not "
        "written to disk by this tool."
    )

    password = getpass.getpass(
        "\nEnter password to audit: "
    )

    if not password:
        print("\n[ERROR] Password cannot be empty.")
        return

    checks = audit_password(password)
    recommendations = generate_recommendations(checks)
    result = determine_result(checks)

    print_audit(
        checks,
        result,
        recommendations,
    )


if __name__ == "__main__":
    main()