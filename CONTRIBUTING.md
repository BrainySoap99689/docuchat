# Contributing to Docuchat

First off, thank you for your interest in contributing to Docuchat! Every contribution—whether it's fixing a bug, improving documentation, or adding a new feature—is appreciated.

## Ways to Contribute

You can contribute by:

* Reporting bugs
* Suggesting new features
* Improving documentation
* Fixing issues
* Improving the user interface
* Optimizing document retrieval or embedding performance
* Adding tests
* Improving Docker or deployment support

Before starting work on a large feature, please open a Feature Request issue to discuss the proposed changes.

---

# Reporting Bugs

If you discover a bug:

1. Search the existing issues to make sure it hasn't already been reported.
2. If it is a new issue, create a **Bug Report** using the provided GitHub issue template.
3. Include:

   * Steps to reproduce
   * Expected behavior
   * Actual behavior
   * Screenshots (if applicable)
   * Error logs
   * Operating system
   * Browser
   * Docker version

The more information you provide, the easier it is to reproduce and fix the issue.

---

# Requesting Features

Feature requests are welcome.

Please describe:

* The problem you are trying to solve
* Your proposed solution
* Why it would improve the project
* Any alternatives you considered

Use the **Feature Request** issue template whenever possible.

---

# Development Setup

## Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/docuchat.git
cd docuchat
```

## Install prerequisites

* Docker Desktop
* Ollama
* Git

Download an Ollama model:

```bash
ollama pull llama3.2
```

Start the project:

```bash
docker compose up --build
```

---

# Branch Naming

Create a new branch for every contribution.

Examples:

```text
feature/chat-history

feature/document-delete

bugfix/vector-search

bugfix/upload-endpoint

docs/readme

refactor/database

test/backend
```

Avoid committing directly to the `main` branch.

---

# Commit Messages

Write meaningful commit messages.

Good:

```text
Add document deletion endpoint

Fix vector similarity query

Improve upload error handling

Update README installation instructions
```

Avoid:

```text
fix

stuff

changes

update
```

---

# Pull Requests

Before submitting a pull request:

* Create a separate branch
* Keep the pull request focused on one change
* Update documentation if necessary
* Test your changes locally
* Ensure the project builds successfully

When opening a pull request:

* Describe what changed
* Reference any related issues
* Include screenshots if the UI changed

---

# Testing

If your change affects functionality:

* Verify the backend starts successfully
* Verify the frontend builds successfully
* Test the affected feature manually

If you add automated tests, ensure they pass before submitting your pull request.

---

# Documentation

Documentation improvements are always welcome.

Please update documentation whenever:

* Adding new features
* Changing APIs
* Changing installation steps
* Modifying Docker configuration

---

# Security

Please **do not** include:

* `.env`
* Passwords
* API keys
* Database credentials
* Personal documents

If you discover a security vulnerability, report it privately using GitHub Security Advisories instead of creating a public issue.

---

# Questions

If you have questions about the project, feel free to open a GitHub Discussion or start a conversation in the project's discussion area.

---

# Thank You

Thank you for helping improve Docuchat!

Every contribution, no matter how small, helps make the project better.
