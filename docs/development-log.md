# Development Log

## Project

Python Security Toolkit

## Purpose

This project is a collection of defensive and educational cybersecurity utilities written in Python. The goal is to strengthen my understanding of secure programming, file integrity, hashing, network communication, log analysis, input validation, automated testing, and technical documentation.

---

## Phase 1 — Development Environment

### Completed

- Installed Python.
- Installed Visual Studio Code.
- Installed the Microsoft Python development extension.
- Installed Git.
- Created a project-specific Python virtual environment.
- Installed pytest for automated testing.

### Technical Decisions

A Python virtual environment is used to isolate project dependencies from the system-wide Python installation.

pytest was selected as the automated testing framework so that individual toolkit components can be validated as development progresses.

### Challenges

PowerShell initially prevented the virtual environment activation script from running because of the system execution policy.

### Resolution

The PowerShell execution policy for the current user was changed to RemoteSigned, allowing locally created scripts such as the virtual environment activation script to execute while retaining restrictions on unsigned downloaded scripts.

### Lessons Learned

Development environment configuration is part of software engineering. Dependency isolation, execution policies, and testing frameworks need to be configured before application development begins.
---

## Phase 2 — SHA-256 Hash Checker

### Objective

Develop the first utility in the Python Security Toolkit: a command-line program capable of calculating the SHA-256 digest of a user-selected file.

### Implementation

The Hash Checker uses Python's built-in `hashlib` module to calculate SHA-256 hashes.

Files are read in 8192-byte chunks rather than loading the entire file into memory. This allows the implementation to remain usable with larger files while keeping memory consumption relatively small.

The `pathlib` module is used for file-path handling and validation.

### Input Validation

Before hashing, the program verifies that:

- The supplied path exists.
- The supplied path represents a file rather than a directory.

### Error Handling

The program handles:

- Missing files
- Invalid file paths
- Permission errors
- General operating-system file errors

Instead of exposing an unhandled Python traceback to the user, the command-line interface returns readable error messages.

### Testing

Automated testing was implemented using pytest.

Current tests validate:

1. Correct SHA-256 calculation.
2. Handling of nonexistent files.
3. Rejection of directories where files are expected.

### Security Concept

Cryptographic hashes provide a deterministic representation of file contents.

Changing the contents of a file produces a different SHA-256 digest, allowing hashes to be used as part of file-integrity verification workflows.

### What I Learned

This phase strengthened my understanding of:

- Python functions
- Binary file operations
- Cryptographic hashing
- SHA-256
- File-path validation
- Exception handling
- Automated testing
- Test isolation using temporary files

### Next Step

Expand the hashing concept into a File Integrity Monitor capable of storing known-good baselines and identifying changed files.

---

## Phase 3 — File Integrity Monitor

### Objective

Develop a defensive file-integrity monitoring utility capable of creating a known-good SHA-256 baseline and identifying subsequent filesystem changes.

### Design

The File Integrity Monitor builds on the SHA-256 functionality developed for the Hash Checker rather than implementing duplicate hashing logic.

The monitor recursively examines a selected directory and stores relative file paths with their SHA-256 digests in a JSON baseline.

### Baseline Process

During baseline creation:

1. The target directory is validated.
2. Files are discovered recursively.
3. SHA-256 hashes are calculated.
4. Relative paths and hashes are stored in JSON.
5. The resulting baseline represents the known-good state of the monitored directory.

### Change Detection

During verification, current file hashes are compared with the stored baseline.

Files are classified as:

- `OK` — file exists and its hash is unchanged.
- `MODIFIED` — file exists but its SHA-256 hash differs.
- `NEW` — file exists but was not present in the baseline.
- `DELETED` — file existed in the baseline but is no longer present.

### Demonstration

A controlled test environment was created containing configuration, report, and administrative files.

After establishing the baseline, the test environment was intentionally changed by:

- Modifying a simulated firewall configuration.
- Introducing a new unapproved file.
- Deleting an existing monitored file.

The monitor successfully identified all three changes while continuing to identify unchanged files correctly.

### Error Handling

The application validates directory and baseline paths and handles:

- Missing directories
- Invalid directory paths
- Missing baseline files
- Invalid baseline paths
- Malformed JSON
- Permission errors
- General filesystem errors

### Automated Testing

pytest tests validate:

- Recursive directory hashing
- Baseline creation
- SHA-256 baseline storage
- Modified-file detection
- New-file detection
- Deleted-file detection
- Missing-directory handling
- Rejection of files where directories are expected
- Invalid JSON handling

The complete project test suite is executed after feature development to verify that newly introduced functionality does not break previously implemented tools.

### Security Concept

File Integrity Monitoring can identify unexpected changes to security-sensitive files by comparing their current cryptographic hashes against previously recorded known-good values.

A hash mismatch does not determine why a file changed or whether the change is malicious. Instead, it provides an integrity signal that can trigger additional investigation.

### Design Limitation

The current implementation uses a manually generated JSON baseline stored locally.

A production-grade integrity monitoring system would require additional protections for the baseline itself, stronger access controls, secure logging, continuous monitoring, and mechanisms to distinguish authorized from unauthorized changes.

### What I Learned

This phase strengthened my understanding of:

- File integrity monitoring
- Known-good baselines
- SHA-256 comparison
- JSON serialization
- Recursive filesystem traversal
- Python dictionaries
- Relative file paths
- Modular code reuse
- Change classification
- Automated regression testing

### Next Step

Develop a security-focused Log Analyzer capable of parsing authentication events and identifying patterns such as repeated failed login attempts.
---

## Phase 4 — Security Log Analyzer

### Objective

Develop a defensive authentication-log analysis utility capable of parsing structured security events and identifying repeated failed-login activity.

### Detection Method

Authentication events are parsed into structured fields containing timestamps, event types, usernames, and source IP addresses.

Failed authentication events are grouped by source IP address. Sources meeting or exceeding a configurable failure threshold generate an alert for further investigation.

### Parser Resilience

Malformed entries are recorded as parser warnings rather than terminating analysis. This allows valid security events to continue being processed even when the source log contains invalid data.

### Security Interpretation

Repeated authentication failures may indicate password guessing, misconfiguration, forgotten credentials, automated processes, or malicious activity.

The detector therefore reports suspicious patterns rather than classifying a source as malicious.

### Automated Testing

Tests validate:

- Authentication-event parsing
- Invalid-entry rejection
- IPv4 validation
- Failed-login counting
- Detection thresholds
- Non-alerting activity below the threshold
- Invalid-line tracking
- Missing-file handling

### What I Learned

This phase strengthened my understanding of:

- Security log parsing
- Regular expressions
- Authentication events
- Python Counter objects
- Event aggregation
- Detection thresholds
- Source-IP analysis
- Parser resilience
- Rule-based security detection

### Next Step

Develop a Password Auditor that evaluates password-policy characteristics without storing or transmitting plaintext credentials.

---

## Phase 5 — Password Auditor

### Objective

Develop a local password-policy auditing utility that evaluates password characteristics and provides actionable security recommendations without storing submitted passwords.

### Security Design

Interactive password entry uses Python's `getpass` functionality so submitted passwords are not echoed to the terminal.

The tool does not write submitted passwords to disk, transmit them over a network, or include them in generated reports.

### Audit Checks

The current implementation evaluates:

- Minimum password length
- Recommended password length
- Uppercase characters
- Lowercase characters
- Numeric characters
- Symbols
- Common-password matches
- Simple predictable sequences
- Repeated consecutive characters

### Results

Rather than assigning an arbitrary numerical security percentage, the tool reports individual policy checks and classifies the result as:

- `STRONG`
- `ACCEPTABLE`
- `NEEDS IMPROVEMENT`

Failed checks generate specific recommendations.

### Limitations

Password composition rules alone cannot accurately measure resistance to every password-guessing strategy.

The common-password dataset used by this educational implementation is intentionally small, and the sequence detector uses simple heuristics.

A production password-security system should consider current organizational policy, compromised-password screening, secure authentication architecture, rate limiting, and multi-factor authentication.

### Automated Testing

Tests validate:

- Common-password detection
- Minimum length requirements
- Character-class requirements
- Sequence detection
- Repeated-character detection
- Strong-password classification
- Recommendation generation

### What I Learned

This phase strengthened my understanding of:

- Secure interactive input
- Password-policy evaluation
- Python string processing
- Character classification
- Security heuristics
- Boolean policy evaluation
- Actionable security reporting
- Limitations of password-strength estimation

### Next Step

Develop a controlled Port Scanner to introduce Python socket programming and network-service discovery within authorized systems and lab environments.
---

## Phase 8 — Authorized Port Scanner

### Objective

Develop a controlled TCP port scanner for identifying listening services on localhost and authorized private-network systems.

### Network Method

The scanner uses Python TCP sockets to attempt connections to a user-selected range of ports.

A successful TCP connection is reported as `OPEN`. An unsuccessful connection is reported as `CLOSED` by this educational implementation.

### Authorization Controls

The scanner deliberately restricts targets to:

- Localhost
- IPv4 loopback addresses
- Private IPv4 networks

Public IP addresses are rejected before scanning begins.

The scanner also limits the maximum requested port range to reduce accidental high-volume scanning.

### Controlled Demonstration

A temporary Python HTTP server was bound to `127.0.0.1` on TCP port `8000`.

The scanner successfully identified port `8000` as open while the service was running.

After stopping the local HTTP server, the scanner identified the same port as closed.

### Limitations

This utility is intentionally simpler than professional scanners such as Nmap.

The current implementation does not attempt:

- Operating-system fingerprinting
- Service-version detection
- SYN scanning
- Firewall evasion
- Stealth techniques
- Vulnerability exploitation

The purpose is to demonstrate TCP socket programming and basic service discovery in a controlled environment.

### Automated Testing

Tests validate:

- Localhost handling
- Private IPv4 authorization
- Public-target blocking
- Invalid target handling
- Port-range validation
- Reversed ranges
- Excessive range rejection
- Socket result handling

### What I Learned

This phase strengthened my understanding of:

- TCP sockets
- IPv4 addressing
- TCP ports
- Connection timeouts
- Private address ranges
- Network authorization boundaries
- Defensive service discovery
- Network error handling

### Next Step

Develop a Network Monitor that reports local network-interface status and traffic statistics without capturing packet contents.

---

## Phase 9 — Local Network Monitor

### Objective

Develop a local network-observability utility capable of reporting interface status, addressing information, and operating-system network traffic counters.

### Implementation

The Network Monitor uses Python's `socket` module and the `psutil` system-utilities library.

The tool gathers:

- System hostname
- Primary local IPv4 address
- Available network interfaces
- Interface UP/DOWN state
- Reported interface speed
- IPv4 addresses
- IPv6 addresses
- Bytes transmitted and received
- Packet counts
- Interface error counters
- Packet-drop counters

### Privacy and Scope

The current implementation does not capture packet payloads or inspect user communications.

Traffic statistics are obtained from operating-system counters rather than packet interception.

### Observability Demonstration

Running the utility at different times produced changing byte and packet counters as network activity occurred, demonstrating that the values are gathered dynamically from the local operating system.

### Dependency Management

The `psutil` library was introduced as the toolkit's first runtime dependency and added to `requirements.txt` so the project's environment can be recreated consistently.

### Limitations

This utility provides a local system-level overview rather than full packet or flow analysis.

It does not currently provide:

- Packet capture
- Protocol decoding
- Remote traffic inspection
- Deep packet inspection
- Intrusion detection
- Historical traffic storage

Future versions could introduce sampling and historical comparison without exposing packet contents.

### Automated Testing

Tests validate:

- Human-readable byte conversion
- Network identity output structure
- Interface information structure
- Traffic-statistics structure
- Nonnegative network counters

Tests avoid expecting specific interface names or addresses so they remain portable across different systems.

### What I Learned

This phase strengthened my understanding of:

- Network interfaces
- IPv4 and IPv6
- Traffic counters
- Interface state
- Network observability
- Python system APIs
- Third-party dependency management
- Portable automated testing

### Next Step

Integrate all toolkit components behind a unified command-line interface.