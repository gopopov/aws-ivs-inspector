import json
import boto3
from decimal import Decimal
from datetime import datetime, timedelta


def respond(err, res=None):
    return {
        "statusCode": "400" if err else "200",
        "body": err.message if err else res,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }


def lambda_handler(event, context):
    print("event:", event)
    cloudWatchClient = boto3.client(
        "cloudwatch", region_name=event["queryStringParameters"]["regionName"]
    )

    # metrics to collect
    metricsToCollect = [
        {"name": "ConcurrentViews", "unit": "Count", "statistics": ["Sum"]},
        {"name": "ConcurrentStreams", "unit": "Count", "statistics": ["Sum"]},
        {"name": "LiveDeliveredTime", "unit": "Seconds", "statistics": ["Sum"]},
        {"name": "LiveInputTime", "unit": "Seconds", "statistics": ["Sum"]},
        {"name": "RecordedTime", "unit": "Seconds", "statistics": ["Sum"]},
    ]

    metrics = []

    for metric in metricsToCollect:
        metrics.append(
            cloudWatchClient.get_metric_statistics(
                Namespace="AWS/IVS",
                MetricName=metric["name"],
                StartTime=datetime.now() - timedelta(hours=24),
                EndTime=datetime.now(),
                Period=60,
                Statistics=metric["statistics"],
                Unit=metric["unit"],
            )
        )

    print(metrics)

    return respond(None, json.dumps(metrics, indent=2, default=str))
