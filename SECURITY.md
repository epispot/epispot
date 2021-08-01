# Security Policy

## Supported Versions

The following versions will receive regular security updates:

| Version | Supported          |
| ------- | ------------------ |
| master-latest   | ✔️ |
| master-2.x.x   | ✔️ |
| nightly-alpha-latest   | ✔️ |
| nightly-latest   | ✔️ |
| master < 2.0   | :x: |
| nightly < latest   | :x: |

## Reporting a Vulnerability

The epispot team works as hard as possible to keep code clear of any vulnerabilities. Our steps include extensive CodeQL analysis, third-party open-source code analysis from tools like DeepSource, and heavy unit testing. However, vulnerabilities will inevitably arise. If you see or suspect a vulnerability, epispot will fix it as fast as possible.

### A note on disclosure:

The entire epispot organization follows [Google's OSS Vulnerability Guide](https://github.com/google/oss-vulnerability-guide) and is committed to eliminating *any* vulnerabilities in our source code. Per [Google's guidelines](https://github.com/google/oss-vulnerability-guide/blob/main/guide.md#response-process), we will disclose any vulnerabilities we find within 90 days of their discovery.

### If you've found a vulnerability:

#### What not to do

**Do not** create an issue, discussion, or any other public notice on the GitHub repository. Please also do not mention the vulnerability publicly in any other projects or channels (that includes official epispot projects as well).

#### I don't have a GitHub account

The simplest way to report a vulnerability is to email the [epispot package authors](https://pypi.org/project/epispot) directly with your concern. The current epispot package author is @quantum9innovation. Send your emails to dev.quantum9innovation@gmail.com and we'll respond as soon as possible. Please include `security`[*](#additional-notes) in the subject line or body of your email so that we can quickly identify the issue.

#### I want to use a GPG key

Please note that we will rarely reply to your email using a GPG key unless it poses a threat to other users and/or packages (this is in line with GitHub's Bug Bounty program, which follows a similar philosophy). If you feel that it is necessary to use a GPG key or want to conceal confidential information, our key fingerprint is:

```text
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
K0Ou
=NenA
-----END PGP PUBLIC KEY BLOCK-----
```

#### I have a GitHub account and ...

##### I don't want to collaborate on a patch

That's completely fine. Simply email us (encrypted or not) and we'll get back to you as soon as possible with our progress.

##### I want to work on the patch

In your email, please include your GitHub username so that we can share with you an invitation to the patch project. The invitation will be to a private GitHub repository that is a fork of the main one. We'll also add you as a collaborator on any public advisories that we will disclose after the patch is committed.

#### Additional Notes

*The word `vulnerability` will also suffice.
