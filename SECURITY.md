# Security Policy

## Supported Versions

The latest `0.1.x` release and the current `main` branch receive security fixes
during the initial public release phase.

## Reporting a Vulnerability

Please do not open a public issue for a vulnerability.

Use GitHub's private vulnerability reporting or Security Advisory feature for
this repository:

https://github.com/anguoyang/inferdoctor/security/advisories/new

Include:

- the affected command or checker;
- the InferDoctor version or commit;
- reproduction steps using sanitized data;
- the expected and actual behavior;
- any proposed mitigation.

Do not include access tokens, private endpoint URLs, credentials, model data,
private hostnames, or full diagnostic reports containing sensitive paths.

InferDoctor is read-only by default, but diagnostic output can still expose
environment details. Review reports before sharing them publicly.
