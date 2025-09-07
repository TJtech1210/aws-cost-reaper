"""Scanning functions for AWS Cost Reaper (read-only, with FAKE fallbacks)."""
from __future__ import annotations

def _use_fake() -> bool:
    import os
    return os.getenv("AWS_COST_REAPER_FAKE", "0") in ("1", "true", "True")

# We import inside functions to avoid hard-failing when boto3 isn't present.
# Each function attempts a real AWS call; on any failure, it returns FAKE data (clearly labeled).
def _use_fake() -> bool:
    """Allow forcing fake mode via env var AWS_COST_REAPER_FAKE=1."""
    import os
    return os.getenv("AWS_COST_REAPER_FAKE", "0") in ("1", "true", "True")


def scan_stopped_ec2_instances(region: str) -> list[dict]:
    """
    Return list[dict]: InstanceId, LaunchTime(ISO), Region for stopped instances.
    On error/lack of perms, returns clearly labeled FAKE data.
    """
    if _use_fake():
        return [
            {"InstanceId": "i-fake123456", "LaunchTime": "2024-01-01T12:00:00Z", "Region": region, "FAKE": True},
            {"InstanceId": "i-fake654321", "LaunchTime": "2024-02-10T08:30:00Z", "Region": region, "FAKE": True},
        ]

    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError

        ec2 = boto3.client("ec2", region_name=region)
        results = []
        paginator = ec2.get_paginator("describe_instances")

        for page in paginator.paginate(
            Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
        ):
            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    results.append(
                        {
                            "InstanceId": instance["InstanceId"],
                            "LaunchTime": instance["LaunchTime"].isoformat(),
                            "Region": region,
                        }
                    )
        return results

    except Exception as e:  # noqa: BLE001 - MVP: catch-all to enable FAKE fallback
        # Fall back to FAKE results (clearly labeled)
        return [
            {
                "InstanceId": "i-fake-noperms",
                "LaunchTime": "2024-03-01T00:00:00Z",
                "Region": region,
                "FAKE": True,
                "ERROR": type(e).__name__,
            }
        ]


def scan_unattached_ebs_volumes(region: str) -> list[dict]:
    """
    Return list[dict]: VolumeId, SizeGiB, CreateTime(ISO), Region for volumes with status=available.
    On error/lack of perms, returns clearly labeled FAKE data.
    """
    if _use_fake():
        return [
            {"VolumeId": "vol-fake111", "SizeGiB": 20, "CreateTime": "2024-01-15T10:00:00Z", "Region": region, "FAKE": True},
            {"VolumeId": "vol-fake222", "SizeGiB": 100, "CreateTime": "2024-02-20T09:45:00Z", "Region": region, "FAKE": True},
        ]

    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError

        ec2 = boto3.client("ec2", region_name=region)
        results = []
        paginator = ec2.get_paginator("describe_volumes")

        for page in paginator.paginate(
            Filters=[{"Name": "status", "Values": ["available"]}]
        ):
            for volume in page.get("Volumes", []):
                results.append(
                    {
                        "VolumeId": volume["VolumeId"],
                        "SizeGiB": volume["Size"],
                        "CreateTime": volume["CreateTime"].isoformat(),
                        "Region": region,
                    }
                )
        return results

    except Exception as e:  # noqa: BLE001
        return [
            {
                "VolumeId": "vol-fake-noperms",
                "SizeGiB": 10,
                "CreateTime": "2024-03-02T00:00:00Z",
                "Region": region,
                "FAKE": True,
                "ERROR": type(e).__name__,
            }
        ]


def scan_unused_elastic_ips(region: str) -> list[dict]:
    """
    Return list[dict]: PublicIp, AllocationId (if present), Region for unassociated Elastic IPs.
    On error/lack of perms, returns clearly labeled FAKE data.
    """
    if _use_fake():
        return [
            {"PublicIp": "203.0.113.10", "AllocationId": "eipalloc-fakeaaa", "Region": region, "FAKE": True},
            {"PublicIp": "203.0.113.20", "AllocationId": None, "Region": region, "FAKE": True},
        ]

    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError

        ec2 = boto3.client("ec2", region_name=region)
        results = []
        paginator = ec2.get_paginator("describe_addresses")

        for page in paginator.paginate():
            for address in page.get("Addresses", []):
                # EIP is unused if it has no association fields present
                if not any(k in address for k in ("AssociationId", "InstanceId", "NetworkInterfaceId")):
                    results.append(
                        {
                            "PublicIp": address["PublicIp"],
                            "AllocationId": address.get("AllocationId"),
                            "Region": region,
                        }
                    )
        return results

    except Exception as e:  # noqa: BLE001
        return [
            {
                "PublicIp": "198.51.100.50",
                "AllocationId": None,
                "Region": region,
                "FAKE": True,
                "ERROR": type(e).__name__,
            }
        ]
