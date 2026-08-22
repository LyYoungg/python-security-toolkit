# Development Log

## Project

Python Security Toolkit

## Purpose

I built the Python Security Toolkit as my first larger programming-focused cybersecurity project.

The goal was not only to get individual scripts working, but to practice building something in stages: setting up a development environment, writing and reusing functions, handling bad input, creating automated tests, debugging mistakes, using Git to track progress, and eventually integrating several tools into one application.

I intentionally kept this development log so the finished repository would show how the project changed over time rather than presenting it as if everything worked correctly on the first attempt.

---

## Phase 1 — Development Environment

### Objective

Set up a clean Python development environment before beginning application development.

### Completed

* Installed Python
* Installed Visual Studio Code
* Installed Microsoft's Python development extension
* Installed Git
* Created a project-specific Python virtual environment
* Installed pytest for automated testing
* Created the initial repository structure

### Technical Decisions

I used a Python virtual environment so project dependencies would remain isolated from the system-wide Python installation.

I selected pytest as the testing framework so that individual tools could be tested as the project grew.

### Challenge — PowerShell Execution Policy

When I first attempted to activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell prevented the script from running because script execution was disabled.

### Resolution

I changed the PowerShell execution policy for the current user to `RemoteSigned`.

This allowed locally created scripts, including the virtual-environment activation script, to run while retaining restrictions on unsigned downloaded scripts.

### What I Learned

This was an early reminder that development is not limited to writing application code.

The operating system, shell, Python environment, dependencies, and security settings all affect whether a project actually works.

---

## Phase 2 — SHA-256 Hash Checker

### Objective

Develop the first utility in the toolkit: a command-line program capable of calculating the SHA-256 digest of a selected file.

### Implementation

The Hash Checker uses Python's built-in `hashlib` module.

Files are opened in binary mode and processed in 8192-byte chunks rather than loading the entire file into memory at once.

The `pathlib` module is used for file-path handling and validation.

### Input Validation

Before hashing, the program verifies that:

* The supplied path exists
* The supplied path represents a file rather than a directory

### Error Handling

The program handles:

* Missing files
* Invalid paths
* Permission errors
* General operating-system file errors

Rather than exposing an unhandled traceback for these expected problems, the CLI returns readable error messages.

### Automated Testing

The first tests validated:

1. Correct SHA-256 calculation
2. Handling of nonexistent files
3. Rejection of directories where files were expected

### Challenge — pytest Module Import Error

When I first ran the automated tests, pytest returned:

```text
ModuleNotFoundError: No module named 'hash_checker'
```

The Hash Checker worked when executed directly, but pytest could not resolve the package correctly during test collection.

### Resolution

I verified that `hash_checker` contained an `__init__.py` file and added a `pytest.ini` configuration file so pytest would treat the repository root as part of Python's module search path and use the correct tests directory.

After saving the configuration and running:

```bash
pytest -v
```

pytest collected the tests correctly.

### What I Learned

This was one of the more useful early mistakes because it showed me that:

> "The script runs" and "the project is structured correctly" are not the same thing.

I learned more about Python packages, imports, module discovery, and how test runners interact with project structure.

### Security Concept

A cryptographic hash gives a deterministic representation of file contents.

If the file changes, its SHA-256 digest changes. That makes hashing useful as part of an integrity-verification process.

---

## Phase 3 — File Integrity Monitor

### Objective

Build on the Hash Checker by creating a utility capable of storing a known-good filesystem state and identifying later changes.

### Design

Instead of writing another SHA-256 implementation, the File Integrity Monitor imports and reuses the `calculate_sha256()` function from the Hash Checker.

This was the first point where the project began to feel less like separate exercises and more like connected software.

### Baseline Process

During baseline creation:

1. The target directory is validated.
2. Files are discovered recursively.
3. Each file receives a SHA-256 hash.
4. Relative paths and hashes are written to JSON.
5. The resulting file becomes the known-good baseline.

### Change Detection

During later verification, files are classified as:

* `OK` — present and unchanged
* `MODIFIED` — present but hash has changed
* `NEW` — present now but absent from the baseline
* `DELETED` — present in the baseline but no longer found

### Controlled Demonstration

I created a test directory containing simulated configuration, report, and administrative files.

After creating a baseline, I intentionally:

* Changed a simulated firewall configuration
* Added a new unapproved file
* Deleted an existing monitored file

The program identified all three changes while continuing to report unchanged files correctly.

### Challenge — Indentation Error

While adding the command-line portion of the File Integrity Monitor, I accidentally placed an extra leading space before:

```python
def main():
```

VS Code marked the line as an error and the program could not be parsed correctly.

### Resolution

I inspected the editor diagnostic, removed the unintended indentation, checked the surrounding function boundaries, saved the file, and reran it.

### What I Learned

The mistake itself was simple, but it reinforced a useful habit: read the specific diagnostic first instead of immediately assuming a large section of code needs to be rewritten.

It also made me more consistent about saving and testing smaller changes as I worked.

### Error Handling

The monitor handles:

* Missing directories
* Invalid directory paths
* Missing baseline files
* Invalid baseline paths
* Malformed JSON
* Permission errors
* General filesystem errors

### Automated Testing

Tests validate:

* Recursive directory hashing
* Baseline creation
* SHA-256 baseline storage
* Modified-file detection
* New-file detection
* Deleted-file detection
* Missing-directory handling
* Rejection of files where directories are expected
* Invalid JSON handling

### Security Limitation

A hash mismatch shows that the contents changed.

It does **not** prove:

* Who changed the file
* Why it changed
* Whether the change was authorized
* Whether the change was malicious

The result is an integrity signal that can prompt further investigation.

The local JSON baseline is also not protected against modification by a sufficiently privileged attacker.

---

## Phase 4 — Security Log Analyzer

### Objective

Develop a defensive authentication-log analysis utility capable of parsing structured events and identifying repeated failed-login activity.

### Implementation

The analyzer processes synthetic authentication events containing:

* Timestamp
* Event type
* Username
* Source IP address

Regular expressions are used to validate and separate each field.

### Detection Method

Failed authentication events are grouped by source IP address.

A configurable threshold determines when repeated failures should generate an alert.

### Parser Resilience

Malformed entries are tracked as warnings rather than causing the entire analysis to terminate.

This means one bad record does not prevent valid events from being analyzed.

### Security Interpretation

Repeated failed logins may indicate:

* Password guessing
* Incorrect saved credentials
* Misconfigured software
* Forgotten passwords
* Automated processes
* Malicious authentication activity

For that reason, the analyzer reports a suspicious pattern rather than claiming that a source is definitely malicious.

### Automated Testing

Tests validate:

* Authentication-event parsing
* Invalid-entry rejection
* IPv4 validation
* Failed-login counting
* Detection thresholds
* Activity below the alert threshold
* Invalid-line tracking
* Missing-file handling

### What I Learned

This phase introduced me to:

* Regular expressions
* Event parsing
* Python `Counter`
* Event aggregation
* Detection thresholds
* Source-IP analysis
* Parser resilience
* Rule-based detection

It also reinforced the difference between detecting an observable pattern and proving malicious intent.

---

## Phase 5 — Password Auditor

### Objective

Create a local password-policy auditing utility that provides useful feedback without intentionally storing submitted passwords.

### Security Design

Interactive password entry uses Python's `getpass` functionality.

That prevents the submitted password from being displayed directly in the terminal while it is entered.

The program does not intentionally:

* Save submitted passwords
* Transmit passwords
* Include submitted passwords in its report

### Audit Checks

The implementation evaluates:

* Minimum length
* Recommended length
* Uppercase characters
* Lowercase characters
* Numeric characters
* Symbols
* Common-password matches
* Simple predictable sequences
* Repeated consecutive characters

### Results

Instead of producing an arbitrary percentage score, the auditor reports individual checks and returns one of three classifications:

* `STRONG`
* `ACCEPTABLE`
* `NEEDS IMPROVEMENT`

Failed checks generate individual recommendations.

### Limitations

Password composition rules alone cannot accurately determine resistance to every password-guessing strategy.

The project's common-password collection and sequence detection are intentionally limited educational implementations.

A production authentication system would need to consider areas such as breached-password screening, rate limiting, organizational policy, secure password storage, and multi-factor authentication.

### Automated Testing

Tests validate:

* Common-password detection
* Minimum-length requirements
* Character-class requirements
* Sequence detection
* Repeated-character detection
* Strong-password classification
* Recommendation generation

### What I Learned

This phase helped me practice:

* Secure interactive input
* String processing
* Character classification
* Security heuristics
* Boolean policy logic
* Actionable reporting
* Recognizing the limits of password-strength rules

---

## Phase 6 — Authorized Port Scanner

### Objective

Develop a controlled TCP port scanner for identifying listening services on localhost and authorized private-network systems.

### Network Method

The scanner uses Python TCP sockets to attempt a connection to each requested port.

For this educational implementation:

* Successful connection → `OPEN`
* Unsuccessful connection → `CLOSED`

### Authorization Controls

The program intentionally restricts targets to:

* `localhost`
* IPv4 loopback addresses
* Private IPv4 addresses

Public IPv4 targets are rejected before scanning begins.

The requested port range is also limited to reduce accidental high-volume scanning.

### Controlled Demonstration

Instead of relying on an unknown external server, I created a temporary local web server with Python on:

```text
127.0.0.1:8000
```

While the service was active, the scanner identified TCP port `8000` as open.

After stopping the HTTP server, I repeated the scan and the port was no longer detected as open.

This gave me a controlled way to test both states.

### Limitations

This tool is intentionally much simpler than a professional scanner such as Nmap.

It does not perform:

* Operating-system fingerprinting
* Service-version detection
* SYN scanning
* Stealth techniques
* Firewall evasion
* Vulnerability exploitation

Its purpose is to demonstrate basic TCP socket programming and service discovery within an authorized environment.

### Automated Testing

Tests validate:

* Localhost handling
* Private IPv4 authorization
* Public-target blocking
* Invalid targets
* Port-range validation
* Reversed port ranges
* Excessive port ranges
* Socket result behavior

### What I Learned

This phase connected Python programming with networking concepts including:

* TCP sockets
* IPv4 addressing
* TCP ports
* Timeouts
* Private address ranges
* Authorization boundaries
* Network error handling

---

## Phase 7 — Local Network Monitor

### Objective

Develop a local network-observability utility capable of reporting interface state, addressing information, and operating-system traffic statistics.

### Implementation

The Network Monitor uses:

* Python's `socket` module
* The `psutil` library

The utility gathers:

* Hostname
* Primary local IP
* Available network interfaces
* Interface UP/DOWN state
* Reported interface speed
* IPv4 addresses
* IPv6 addresses
* Bytes sent and received
* Packet counts
* Error counters
* Packet-drop counters

### Privacy and Scope

The monitor does not capture packet payloads or inspect communications.

It reads statistics already maintained by the operating system.

### Dependency Management

`psutil` became the first third-party runtime dependency in the project.

I added it to `requirements.txt` so another user can recreate the project's dependency environment without manually identifying each package.

### Portable Testing

Network configurations vary from computer to computer.

Instead of writing tests that assumed my machine would always have an interface named `Ethernet` or a particular IP address, the tests validate the structure and type of the returned data.

That makes the test suite less dependent on my own computer.

### Limitations

The utility does not currently provide:

* Packet capture
* Protocol decoding
* Remote traffic inspection
* Deep packet inspection
* Intrusion detection
* Historical traffic storage

### What I Learned

This phase helped me understand:

* Network interfaces
* IPv4 and IPv6
* Traffic counters
* Interface state
* Network observability
* Python system APIs
* Dependency management
* Portable testing

---

## Phase 8 — Unified Command-Line Interface

### Objective

Combine the independently developed utilities into one application without rewriting each tool inside a single large file.

### Architecture

Each utility remains an independent Python module.

The root-level:

```text
securitytool.py
```

imports the entry point from each module and exposes the tools through one menu.

### Available Components

The unified interface provides:

1. SHA-256 Hash Checker
2. File Integrity Monitor
3. Security Log Analyzer
4. Password Auditor
5. Authorized Port Scanner
6. Local Network Monitor

### Design

A dictionary-based dispatcher maps menu choices to the correct utility.

This keeps the central CLI relatively small and makes future additions easier than placing all tool logic directly inside the menu program.

### User Experience

The application:

* Provides one command to launch the toolkit
* Returns to the main menu after a utility finishes
* Handles invalid menu choices without terminating
* Keeps each underlying utility usable independently

### Regression Testing

After integration, I reran the complete pytest suite to verify that connecting the modules through the unified interface had not broken earlier functionality.

### What I Learned

This phase helped me understand:

* Module integration
* Function imports and aliases
* Application entry points
* Dictionary-based dispatch
* Command-line application design
* Modular architecture
* Regression testing

---

## Final Project Reflection

This was my first project where I tried to treat the work as more than a set of finished Python exercises.

At the beginning, even setting up the environment required learning things I had not expected to be part of the project. As it grew, I encountered problems involving PowerShell, Python imports, pytest configuration, syntax and indentation, filesystem handling, dependencies, networking, and module integration.

I decided to keep those problems in this log because they are part of what I actually learned.

The project gradually changed from:

```text
individual script
        ↓
another individual script
        ↓
shared functionality
        ↓
automated testing
        ↓
security boundaries
        ↓
multiple modules
        ↓
one integrated application
```

The finished toolkit is intentionally not presented as production security software. Each component has limitations, and those limitations are documented throughout the project.

What I gained from building it was practical experience connecting several areas that I had previously encountered separately:

* Python programming
* Cryptographic hashing
* File integrity
* Security log analysis
* Password policy
* TCP networking
* Network interfaces
* Input validation
* Exception handling
* Automated testing
* Git version control
* Dependency management
* Technical documentation
* Modular software design

One of the most useful lessons was realizing that getting output from a program is only one part of building software. I also had to think about how another person would install it, what happens when input is wrong, how one module can reuse another, how tests should behave on a different computer, what security conclusions the program can reasonably support, and how to document what the project cannot do.

For a future project, I want to apply those lessons from the beginning instead of discovering all of them halfway through development.
