## Testing Challenge — Module Import Error

My first attempt to run the automated Hash Checker tests did not succeed.

pytest returned:

```text
ModuleNotFoundError: No module named 'hash_checker'
```

The Hash Checker itself could run directly, but the test runner was not resolving the package correctly from the project structure.

### Resolution

I verified the package structure and added a `pytest.ini` configuration file that defines the project root for Python imports and identifies the `tests` directory.

After saving the configuration and rerunning:

```bash
pytest -v
```

the tests were collected correctly and passed.

### What I Learned

This was the first point in the project where I realized that code working when executed directly does not necessarily mean the project is configured correctly for imports and automated testing.

It helped me understand the relationship between Python packages, project structure, module discovery, and test configuration.

---

## Development Challenge — File Integrity Monitor Syntax Error

While adding the File Integrity Monitor, I introduced an indentation error before the `main()` function.

VS Code identified the problem before the program could run correctly.

The issue was caused by an extra leading space before:

```python
def main():
```

### Resolution

I corrected the indentation, reviewed the surrounding function boundaries, saved the file, and reran the program before continuing with testing.

### What I Learned

Although the error itself was small, it reinforced the importance of reading editor diagnostics carefully instead of immediately rewriting larger portions of working code.

It also made me more consistent about saving and testing after smaller changes.

---

## Final Project Reflection

This was my first project where I tried to treat the work as more than a collection of completed Python exercises.

I began with very basic setup tasks, including creating a virtual environment and learning how Git tracked files. As the project grew, I had to deal with issues I did not expect at the beginning: PowerShell execution policies, Python import paths, pytest configuration, file handling, malformed input, network restrictions, dependencies, and eventually integrating multiple modules into one interface.

The most useful part of the project was not that every component eventually worked. It was seeing how the project changed as I understood more about what I was building.

The early tools were mostly isolated. Later tools reused earlier functionality, introduced clearer security boundaries, and had tests designed to avoid depending too heavily on my own computer.

There are still many things I would improve in a production system, and I have tried to document those limitations throughout the project rather than presenting the toolkit as something it is not.

The final version gave me practical experience with:

* Python project organization
* Defensive cybersecurity concepts
* Cryptographic hashing
* File-integrity monitoring
* Authentication-log analysis
* Password-policy auditing
* TCP networking
* Network-interface monitoring
* Input validation
* Error handling
* Automated testing
* Git version control
* Dependency management
* Technical documentation
* Integrating multiple modules into one application

The project also gave me a much clearer idea of what I want to improve in future work: better abstraction, more flexible configuration, stronger testing, and projects that connect programming even more closely with real security environments.

### Phase Numbering

For the final public development log, use the following sequence:

1. Development Environment
2. SHA-256 Hash Checker
3. File Integrity Monitor
4. Security Log Analyzer
5. Password Auditor
6. Authorized Port Scanner
7. Local Network Monitor
8. Unified Command-Line Interface
