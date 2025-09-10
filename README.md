# AWS Cost Reaper

**A Python CLI tool to identify (and soon clean up) unused AWS resources.**

AWS Cost Reaper helps reduce unnecessary cloud spend by detecting idle EC2 resources in your AWS environment. Built with Boto3, it's designed for safe analysis with a dry-run default and a local FAKE mode for testing without credentials.

---

## Features

* Detects:

  * Stopped EC2 instances
  * Unattached EBS volumes
  * Unused Elastic IPs
* Output formats: `table` or `json`
* **Dry-run mode by default** — no deletions performed
* **FAKE mode** for safe local testing without AWS access (`AWS_COST_REAPER_FAKE=1`)
* Structured as a standard Python package: `cost_reaper/`

---

## Setup

Clone the repository:

```bash
git clone https://github.com/TJtech1210/aws-cost-reaper.git
cd aws-cost-reaper
```

Create and activate a virtual environment:

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Run in FAKE mode (no AWS credentials required)

```bash
export AWS_COST_REAPER_FAKE=1
python -m cost_reaper.cli --scan --region us-east-1 --report table
```

Or for JSON output:

```bash
python -m cost_reaper.cli --scan --region us-east-1 --report json
```

### Sample Output (Table)

```
== Stopped EC2 Instances ==
i-fake123456  launched=2024-01-01T12:00:00Z  region=us-east-1  FAKE

== Unattached EBS Volumes ==
vol-fake111  sizeGiB=20  created=2024-01-15T10:00:00Z  region=us-east-1  FAKE

== Unused Elastic IPs ==
203.0.113.10  allocationId=eipalloc-fakeaaa  region=us-east-1  FAKE
```

---

## Required AWS Permissions

For real scans (not using FAKE mode), the following IAM permissions are required:

* `ec2:DescribeInstances`
* `ec2:DescribeVolumes`
* `ec2:DescribeAddresses`

You can attach the AWS-managed **ReadOnlyAccess** policy or create a minimal custom policy with just these actions.

---

## Roadmap

* Add `--cleanup` and `--force` flags for safe resource deletion
* Rich CLI output with colorized tables (`rich` library)
* Unit test suite with mock AWS clients for CI/CD integration
* Extend support to:

  * RDS snapshots
  * Unused IAM users
  * More AWS resource types

---

**Contributions and feedback are welcome.**
If this tool helped you reduce AWS costs or spot forgotten resources, let me know or share the repo!
