from password_auditor.password_auditor import (
    audit_password,
    contains_repeated_characters,
    contains_sequence,
    determine_result,
    generate_recommendations,
)


def test_common_password_detected():
    checks = audit_password("password")

    assert checks["not_common"] is False


def test_short_password_detected():
    checks = audit_password("Ab1!")

    assert checks["minimum_length"] is False


def test_missing_uppercase_detected():
    checks = audit_password("lowercase!12345")

    assert checks["uppercase"] is False


def test_missing_symbol_detected():
    checks = audit_password("SecurePassword12345")

    assert checks["symbol"] is False


def test_simple_sequence_detected():
    assert contains_sequence("Secure123!Password") is True


def test_repeated_characters_detected():
    assert contains_repeated_characters(
        "Secure!!!Password7"
    ) is True


def test_strong_password():
    password = "Cedar!Orbit7-Lantern"

    checks = audit_password(password)
    result = determine_result(checks)

    assert result == "STRONG"


def test_recommendations_generated():
    checks = audit_password("password")

    recommendations = generate_recommendations(checks)

    assert len(recommendations) > 0