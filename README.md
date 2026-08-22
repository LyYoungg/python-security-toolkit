# Python Security Toolkit

A modular collection of defensive cybersecurity utilities written in Python.

This project is being developed to explore practical applications of secure programming, hashing, file integrity monitoring, log analysis, network communication, password auditing, automated testing, and command-line application design.

> **Status:** Active development

## Planned Tools
- [x] Hash Checker
- [x] File Integrity Monitor
- [x] Log Analyzer
- [x] Password Auditor
- [x] Port Scanner
- [ ] Network Monitor
- [ ] Unified Command-Line Interface

## Current Development Stage

## Current Development Stage

Two defensive security utilities are currently implemented:

### SHA-256 Hash Checker

Calculates SHA-256 file hashes with file validation, exception handling, and automated tests.

### File Integrity Monitor

Creates JSON-based known-good file baselines and detects unchanged, modified, newly introduced, and deleted files through SHA-256 comparison.

The next planned component is the Log Analyzer.
## Project Goals

The toolkit is designed to demonstrate:

- Python programming
- Defensive security concepts
- Secure file handling
- SHA-256 hashing
- JSON processing
- Network programming
- Log analysis
- Input validation
- Error handling
- Automated testing with pytest
- Git version control
- Technical documentation

## Repository Structure

```text
python-security-toolkit/
├── docs/
├── hash_checker/
├── tests/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

### Security Log Analyzer
Parses synthetic authentication events, summarizes login activity, tracks failed authentication attempts by source IP, and generates threshold-based alerts for suspicious patterns.


### Password Auditor
Evaluates password-policy characteristics locally, identifies common weaknesses and predictable patterns, and generates security recommendations without storing or displaying submitted passwords.

### Authorized Port Scanner
Performs controlled TCP connection checks against localhost and authorized private IPv4 systems. Public targets and excessive scan ranges are deliberately blocked by the application.