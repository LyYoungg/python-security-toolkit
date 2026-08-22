# Architecture

## Overview

The Python Security Toolkit is organized as a set of independent defensive-security utilities connected through one command-line interface.

I did not begin the project with this full architecture already designed. The structure developed as I added tools and realized that keeping each feature separate made the code easier to test, troubleshoot, and understand.

The final design keeps individual security functions inside their own packages while using `securitytool.py` as the main entry point.

## High-Level Structure

```text
                         securitytool.py
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
       Hash Checker     File Integrity    Log Analyzer
                             Monitor
             |
             +------ reusable SHA-256 function ------+
                                                     |
             +----------------+----------------------+
             |                |                      |
             v                v                      v
     Password Auditor    Port Scanner          Network Monitor
```

The exact tools do not all depend on one another. The diagram represents their relationship to the unified interface and highlights the intentional reuse of the hashing implementation.

## Entry Point

The primary user-facing entry point is:

```text
securitytool.py
```

Running:

```bash
python securitytool.py
```

opens the main menu.

The file imports the `main()` function from each utility and assigns a clear alias to each one.

A dictionary-based dispatcher maps the user's selection to the appropriate function.

This keeps the menu code separate from the implementation of each security tool.

## Module Responsibilities

### `hash_checker`

Calculates SHA-256 hashes for individual files.

It handles:

* Path validation
* Binary file reading
* Chunked hashing
* File-related exceptions

Its `calculate_sha256()` function is reused by the File Integrity Monitor.

### `file_integrity_monitor`

Creates and loads JSON-based file-integrity baselines.

It is responsible for:

* Recursive directory discovery
* SHA-256 baseline generation
* Relative path storage
* Comparison of current and baseline state
* `OK`, `MODIFIED`, `NEW`, and `DELETED` classifications

Separating the hashing function from the integrity-monitoring logic avoids maintaining two independent SHA-256 implementations.

### `log_analyzer`

Processes synthetic authentication events.

It is responsible for:

* Parsing log entries
* Separating valid and invalid entries
* Counting successful and failed authentication events
* Grouping failures by source IP
* Applying a configurable detection threshold
* Producing rule-based alerts

The analyzer reports activity that deserves attention but does not attempt to determine intent.

### `password_auditor`

Performs local password-policy evaluation.

It checks characteristics including:

* Length
* Character classes
* Common-password matches
* Predictable sequences
* Repeated characters

Interactive input uses `getpass`, and the password is not intentionally written to disk or transmitted.

### `port_scanner`

Performs basic TCP connection checks.

It is responsible for:

* IPv4 target validation
* Restricting targets to localhost and private networks
* Port-range validation
* TCP connection attempts
* Reporting basic open/closed results

The restrictions are part of the module's design rather than only documentation.

### `network_monitor`

Reads network information available from the local operating system.

It reports:

* Host information
* Interface information
* IPv4 and IPv6 addresses
* Interface state
* Traffic counters
* Error and packet-drop counters

It uses `psutil` for system network information and does not inspect packet payloads.

## Testing Structure

Automated tests live in:

```text
tests/
```

Each major module has a corresponding test file.

The tests are designed around behavior that should remain predictable across systems where possible.

For example, the Network Monitor tests do not assume that every computer has an interface named `Ethernet`. Instead, they verify that returned interface records follow the data structure expected by the application.

This makes the tests less dependent on my own computer.

The complete test suite is run with:

```bash
pytest -v
```

I used the full suite after adding new modules so that earlier functionality could be checked for regressions.

## Dependency Management

Most of the toolkit uses Python's standard library.

Examples include:

* `hashlib`
* `json`
* `pathlib`
* `socket`
* `ipaddress`
* `re`
* `getpass`
* `collections`

The Network Monitor requires the third-party `psutil` package.

Project dependencies are listed in:

```text
requirements.txt
```

A local `.venv` environment is used during development but is excluded from Git.

## Error Handling

A design goal across the toolkit is to handle predictable user and filesystem errors without dumping unnecessary tracebacks into the normal command-line interface.

Examples include:

* Missing files
* Missing directories
* Invalid paths
* Invalid menu selections
* Malformed log entries
* Invalid JSON
* Invalid IP addresses
* Invalid port ranges
* Permission errors

This does not mean every possible failure condition is covered. It means that common expected errors are handled deliberately instead of being left entirely to Python's default exception output.

## Security Boundaries

Some restrictions are implemented directly in the code.

### Port Scanner

The scanner permits:

* `localhost`
* Loopback IPv4 addresses
* Private IPv4 addresses

Public IPv4 targets are rejected.

The number of ports in a requested scan is also limited.

### Password Auditor

Password input is hidden using `getpass`.

The submitted value is used for local analysis and is not intentionally persisted by the program.

### Network Monitor

The monitor reads operating-system counters and interface information.

It does not perform packet capture or inspect packet contents.

### Example Data

Authentication logs and file-integrity demonstrations use synthetic data rather than real credentials or real security incidents.

## Design Philosophy

My main goal was not to build the largest possible security toolkit. I wanted to build something I could understand from end to end.

That influenced several decisions.

### Keep the modules small enough to understand

Each utility has a narrow responsibility. This made it easier for me to identify where problems were coming from and write tests around specific behavior.

### Reuse working code instead of copying it

The File Integrity Monitor uses the Hash Checker's SHA-256 function instead of maintaining a second implementation.

That was one of the first points in the project where I started thinking about the relationship between modules instead of only about making an individual script work.

### Validate before acting

Several tools check input before performing file or network operations.

This is especially visible in the Port Scanner, where authorization boundaries are enforced in the program rather than being left only as a warning in the README.

### Prefer understandable output over unnecessary complexity

The tools report enough information to demonstrate their security purpose without pretending to offer the depth of mature products such as Nmap, a SIEM, EDR software, or enterprise integrity-monitoring platforms.

### Test behavior, not my specific computer

Where possible, the automated tests check expected structures and logic rather than hard-coding values that are unique to my machine.

### Document limitations

One lesson from building the project was that successful output does not automatically mean a security conclusion is justified.

For example:

* A changed hash proves that file content changed, but not why.
* Failed logins can be suspicious, but they do not prove an attack.
* A successful TCP connection indicates that something accepted a connection, but it does not identify every detail about the service.
* Password composition checks provide useful feedback but cannot perfectly measure resistance to password guessing.

I wanted those limitations to be visible rather than hiding them behind stronger-sounding claims.

## Development Lessons That Influenced the Architecture

The architecture was also shaped by problems I encountered during development.

Early on, PowerShell prevented the virtual-environment activation script from running because of the execution policy.

Later, pytest produced a `ModuleNotFoundError` because my project package was not being resolved correctly during test collection. Adding and understanding the pytest configuration helped me see why project layout matters beyond simply placing Python files into folders.

I also ran into smaller syntax and indentation mistakes while adding functions. Those were simple errors, but they reinforced the value of saving frequently, reading editor diagnostics, and testing each stage before moving on.

By the time the unified interface was added, the project already had separate modules and tests. That made integration much easier than it would have been if everything had been written inside one large Python file.

## Current Limitations

The architecture is intentionally appropriate for a learning project.

It does not currently include:

* A graphical interface
* Persistent application configuration
* Centralized structured logging
* Asynchronous networking
* Plugin discovery
* Protected integrity baselines
* Remote agents
* Database storage
* Production authentication controls

Those would increase complexity substantially and are outside the current scope.

## Future Architecture Ideas

If the project grows, possible improvements include:

* A shared configuration module
* Common output/report formatting
* Structured JSON report export
* A dedicated exception hierarchy
* Packaging with `pyproject.toml`
* An installable console command
* Historical network-statistics storage
* Support for additional log formats

The current structure provides a reasonable foundation for those changes without requiring them for the first version of the project.
