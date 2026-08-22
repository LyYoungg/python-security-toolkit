# Python Security Toolkit

A modular collection of defensive cybersecurity utilities built in Python.

I started this project to get more comfortable writing Python while connecting what I was learning in cybersecurity to something I could actually build and test myself. Instead of trying to create one large application all at once, I built each utility separately, tested it, documented problems I ran into, and then brought everything together behind one command-line interface.

The result is a small defensive security toolkit focused on file integrity, authentication logs, password auditing, TCP networking, and local network visibility.

## Project Status

**Complete — Initial Portfolio Release**

Current tools:

* [x] SHA-256 Hash Checker
* [x] File Integrity Monitor
* [x] Security Log Analyzer
* [x] Password Auditor
* [x] Authorized Port Scanner
* [x] Local Network Monitor
* [x] Unified Command-Line Interface

## What It Includes

### SHA-256 Hash Checker

Calculates the SHA-256 digest of a selected file.

The tool includes:

* File-path validation
* Binary file handling
* Chunked file reading
* SHA-256 hashing
* Error handling
* Automated tests

The hashing function is also reused by the File Integrity Monitor rather than being rewritten in multiple places.

### File Integrity Monitor

Creates a known-good JSON baseline for a directory and later compares the current filesystem state against that baseline.

Files are classified as:

* `OK`
* `MODIFIED`
* `NEW`
* `DELETED`

This part of the project helped me understand how cryptographic hashes can be used as an integrity signal rather than simply as isolated hash values.

### Security Log Analyzer

Parses synthetic authentication logs and summarizes login activity.

It can:

* Parse successful and failed authentication events
* Track failed logins by source IP
* Apply a configurable detection threshold
* Identify usernames targeted by repeated failures
* Continue processing when malformed log entries are encountered

The analyzer reports suspicious patterns rather than automatically declaring that an address is malicious. Repeated failed logins can have legitimate causes, so an alert is treated as something that deserves further investigation.

### Password Auditor

Evaluates password-policy characteristics locally and provides specific recommendations.

Checks include:

* Minimum and recommended length
* Uppercase and lowercase characters
* Numbers
* Symbols
* Common-password matches
* Simple predictable sequences
* Repeated characters

Interactive input uses Python's `getpass` functionality so the entered password is not displayed in the terminal. The program does not intentionally save or transmit submitted passwords.

### Authorized Port Scanner

Performs basic TCP connection checks against localhost and private IPv4 systems.

The scanner includes several intentional restrictions:

* Public IPv4 targets are blocked
* Scan ranges are limited
* Input is validated before network activity begins
* The tool is intended for localhost, private lab environments, and systems where testing is authorized

For testing, I created a temporary Python HTTP server on `127.0.0.1:8000`, verified that the scanner detected the port while the service was running, stopped the server, and confirmed that the same port was no longer reported as open.

### Local Network Monitor

Reports information available from the local operating system, including:

* Hostname
* Local addressing
* Network interfaces
* Interface status
* IPv4 and IPv6 addresses
* Reported interface speed
* Bytes sent and received
* Packet counters
* Error counters
* Drop counters

It uses local system statistics rather than capturing network packet contents.

## Unified Interface

All six utilities can be launched from one entry point:

```bash
python securitytool.py
```

The menu provides:

```text
============================================================
                 PYTHON SECURITY TOOLKIT
============================================================

Defensive Security & System Analysis Utilities

[1] SHA-256 Hash Checker
[2] File Integrity Monitor
[3] Security Log Analyzer
[4] Password Auditor
[5] Authorized Port Scanner
[6] Local Network Monitor

[0] Exit
```

Each utility can still be run and tested independently, while the unified interface gives the project a single user-facing entry point.

## Quick Installation

You do **not** need to rebuild the toolkit from scratch to use it.

You only need Python, Git, and the files in this repository.

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd python-security-toolkit
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Toolkit

```bash
python securitytool.py
```

That's it.

The detailed setup and development process in the development log documents how I built the project; users do not need to repeat those steps simply to run it.

## Testing

The project uses `pytest` for automated testing.

Run the complete test suite with:

```bash
pytest -v
```

Tests cover areas including:

* SHA-256 calculation
* Missing and invalid file paths
* File-integrity baseline creation
* Modified, new, and deleted file detection
* Authentication-log parsing
* Detection thresholds
* Invalid log entries
* Password-policy checks
* Port-target restrictions
* Port-range validation
* Network-information data structures
* Unified menu validation

I reran the complete test suite as new modules were added so changes to one part of the toolkit would not silently break earlier functionality.

## Repository Structure

```text
python-security-toolkit/
├── docs/
│   ├── architecture.md
│   └── development-log.md
│
├── examples/
│   ├── authentication.log
│   └── integrity_demo/
│
├── file_integrity_monitor/
├── hash_checker/
├── log_analyzer/
├── network_monitor/
├── password_auditor/
├── port_scanner/
│
├── tests/
│   ├── test_file_integrity_monitor.py
│   ├── test_hash_checker.py
│   ├── test_log_analyzer.py
│   ├── test_network_monitor.py
│   ├── test_password_auditor.py
│   ├── test_port_scanner.py
│   └── test_securitytool.py
│
├── .gitignore
├── LICENSE
├── pytest.ini
├── README.md
├── requirements.txt
└── securitytool.py
```

## Documentation

This README is intentionally an overview rather than a complete record of every development step.

For more detail:

* [`docs/development-log.md`](docs/development-log.md) documents the project chronologically, including problems I encountered and how I fixed them.
* [`docs/architecture.md`](docs/architecture.md) explains how the modules fit together and why I structured the project this way.

## Security and Ethical Scope

This is an educational defensive-security project.

The Port Scanner is intentionally restricted to localhost and private IPv4 systems and should only be used on systems the operator owns or has permission to test.

The Password Auditor performs local evaluation and does not intentionally store submitted passwords.

The Network Monitor reads operating-system statistics rather than packet payloads.

The project does not contain exploitation functionality, credential cracking, stealth-scanning features, or mechanisms designed to bypass security controls.

## Limitations

This toolkit is not intended to replace production security platforms.

Some intentional limitations include:

* The File Integrity Monitor stores its baseline locally and does not protect that baseline from a privileged attacker.
* The Log Analyzer uses straightforward rule-based thresholds rather than behavioral analytics.
* The Password Auditor uses heuristics and a limited common-password list rather than a breached-password service.
* The Port Scanner performs basic TCP connection checks rather than advanced service fingerprinting.
* The Network Monitor reports local system statistics rather than packet or flow analysis.

I chose to document these limitations because understanding what a security tool cannot tell you is just as important as understanding what it can.

## What I Learned

The biggest thing I learned from this project was how much work exists around the actual feature code.

I expected most of the challenge to be writing Python. Instead, a large part of the learning came from configuring environments, understanding imports, debugging tests, validating user input, deciding where functionality should live, handling errors cleanly, keeping the repository organized, and making sure new changes did not break previous work.

It also helped me connect programming concepts to cybersecurity concepts I had previously encountered separately, especially hashing, file integrity, authentication events, TCP ports, and network interfaces.

## Future Improvements

Possible future improvements include:

* Support for additional structured log formats
* Configuration files for thresholds and policies
* More metadata in file-integrity baselines
* Historical network-statistics sampling
* Expanded common-password screening
* Additional automated tests
* Packaging the toolkit as an installable Python application

For now, the goal of this release is to keep the toolkit understandable, testable, and clearly scoped rather than adding features simply to make it larger.

## License

This project is available under the MIT License.
