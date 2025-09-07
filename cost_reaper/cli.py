"""Command-line interface for AWS Cost Reaper."""
from __future__ import annotations

import argparse
import json
from typing import Dict, Any

from . import scanner



def _to_json(results: Dict[str, Any]) -> str:
    return json.dumps(results, indent=2, sort_keys=True)


def _to_table(results: Dict[str, Any]) -> str:
    lines = []
    # Section: EC2 stopped
    ec2 = results.get("ec2_stopped", [])
    lines.append("== Stopped EC2 Instances ==")
    if not ec2:
        lines.append("(none)")
    else:
        for r in ec2:
            lines.append(f"- {r.get('InstanceId')}  launched={r.get('LaunchTime')}  region={r.get('Region')}{'  FAKE' if r.get('FAKE') else ''}")
    lines.append("")

    # Section: EBS unattached
    ebs = results.get("ebs_unattached", [])
    lines.append("== Unattached EBS Volumes ==")
    if not ebs:
        lines.append("(none)")
    else:
        for r in ebs:
            lines.append(f"- {r.get('VolumeId')}  sizeGiB={r.get('SizeGiB')}  created={r.get('CreateTime')}  region={r.get('Region')}{'  FAKE' if r.get('FAKE') else ''}")
    lines.append("")

    # Section: Unused EIPs
    eips = results.get("eip_unused", [])
    lines.append("== Unused Elastic IPs ==")
    if not eips:
        lines.append("(none)")
    else:
        for r in eips:
            alloc = r.get("AllocationId") or "None"
            lines.append(f"- {r.get('PublicIp')}  allocationId={alloc}  region={r.get('Region')}{'  FAKE' if r.get('FAKE') else ''}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cost-reaper",
        description="Scan for unused AWS resources (read-only).",
    )
    parser.add_argument("--scan", action="store_true", help="Run scanners (EC2/EBS/EIP).")
    parser.add_argument("--region", default="us-east-1", help="AWS region to scan (default: us-east-1).")
    parser.add_argument("--report", choices=["json", "table"], default="table", help="Output format.")
    args = parser.parse_args()

    if not args.scan:
        parser.print_help()
        return

    # Call scanners (read-only)
    results = {
        "ec2_stopped": scanner.scan_stopped_ec2_instances(args.region),
        "ebs_unattached": scanner.scan_unattached_ebs_volumes(args.region),
        "eip_unused": scanner.scan_unused_elastic_ips(args.region),
    }

    if args.report == "json":
        print(_to_json(results))
    else:
        print(_to_table(results))


if __name__ == "__main__":
    main()
