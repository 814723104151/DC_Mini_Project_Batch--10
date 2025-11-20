import os
import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("EXAMS_TABLE", "ExamsTable")
table = dynamodb.Table(TABLE_NAME)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body, default=decimal_default)
    }

def iso_now():
    return datetime.utcnow().isoformat() + "Z"
