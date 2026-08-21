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
