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