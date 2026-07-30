# Security Policy

Thank you for helping keep Docuchat secure.

We take security seriously and appreciate responsible disclosure of potential vulnerabilities.

## Supported Versions

Security updates are provided for the latest version of the project under active development.

| Version              | Supported |
| -------------------- | :-------: |
| Latest `main` branch |     ✅     |
| Older releases       |     ❌     |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, use one of the following methods:

1. **GitHub Security Advisories (preferred)**

   * Navigate to the repository's **Security** tab.
   * Select **Report a vulnerability**.
   * Submit a private vulnerability report.

2. **Email** 

   You may report vulnerabilities privately by email to aryavikrampingali@gmail.com

## What to Include

Please include as much information as possible, including:

* Description of the vulnerability
* Steps to reproduce
* Proof of concept (if available)
* Potential impact
* Suggested mitigation (optional)
* Environment details

  * Operating system
  * Browser (if applicable)
  * Docker version
  * Python version
  * Ollama version

Screenshots and logs are appreciated when relevant.

## Response Process

After receiving a report, we will:

* Acknowledge receipt as soon as reasonably possible.
* Investigate and validate the report.
* Work on a fix if the issue is confirmed.
* Credit the reporter (with permission) when appropriate.

Response times may vary depending on the severity and complexity of the issue.

## Responsible Disclosure

Please allow reasonable time for a fix before publicly disclosing a vulnerability.

Avoid publicly sharing exploit details until the issue has been addressed.

## Scope

Examples of issues that may be considered security vulnerabilities include:

* Remote code execution
* Authentication or authorization bypass
* Sensitive data exposure
* SQL injection
* Command injection
* Cross-site scripting (XSS)
* Cross-site request forgery (CSRF)
* Arbitrary file upload or file read
* Path traversal
* Docker container escape
* Dependency vulnerabilities that create a practical security risk

## Out of Scope

The following are generally not considered security vulnerabilities:

* Typographical errors
* Documentation mistakes
* Feature requests
* Missing functionality
* Minor user interface issues
* Denial-of-service concerns requiring unrealistic resources
* Vulnerabilities in unsupported third-party software or operating systems

## Secrets

Please **never** include any of the following in issues, pull requests, or discussions:

* `.env` files
* Database passwords
* API keys
* Authentication tokens
* Private documents
* Personally identifiable information (PII)

If you accidentally commit a secret, remove it immediately, rotate the credential if applicable, and notify the maintainers privately.

## Thank You

Thank you for helping make Docuchat safer for everyone.
