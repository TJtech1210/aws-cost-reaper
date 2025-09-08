# AWS Cost Reaper

A brutal Python CLI tool to **find (and later clean up)** unused AWS resources.  
- Built with [Boto3](https://boto3.amazonaws.com/).  
- Default is **dry-run**: **no deletions** unless you explicitly enable cleanup (future version).  
- Includes **FAKE mode** so you can demo/test even without AWS credentials.  

---

## 🚀 Features
- Scan for:
  - Stopped **EC2 instances**
  - Unattached **EBS volumes**
  - Unused **Elastic IPs**
- Output in **table** or **JSON** format  
- **FAKE mode** (`AWS_COST_REAPER_FAKE=1`) for safe local testing  
- Structured as a proper Python package (`cost_reaper/`)  

---

## ⚙️ Setup

Clone the repo:

git clone https://github.com/TJtech1210/aws-cost-reaper.git
cd aws-cost-reaper

Create a virtual environment:

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows PowerShell


Install dependencies:

pip install -r requirements.txt

🖥️ Usage

FAKE mode demo (no AWS required):

export AWS_COST_REAPER_FAKE=1
python -m cost_reaper.cli --scan --region us-east-1 --report table
python -m cost_reaper.cli --scan --region us-east-1 --report json


Example output (table):

== Stopped EC2 Instances ==
- i-fake123456  launched=2024-01-01T12:00:00Z  region=us-east-1  FAKE

== Unattached EBS Volumes ==
- vol-fake111  sizeGiB=20  created=2024-01-15T10:00:00Z  region=us-east-1  FAKE

== Unused Elastic IPs ==
- 203.0.113.10  allocationId=eipalloc-fakeaaa  region=us-east-1  FAKE

🔒 AWS Permissions Required (for real scans)

When not in FAKE mode, the following IAM actions are required:

ec2:DescribeInstances

ec2:DescribeVolumes

ec2:DescribeAddresses

Attach either the AWS managed ReadOnlyAccess policy or a custom policy with those actions.

🛣️ Roadmap

 Add cleanup mode (--cleanup --force) for safe deletions

 Rich table output with colors (rich library)

 Unit tests with mocks for CI/CD

 Support for more resource types (RDS snapshots, unused IAM users, etc.)


