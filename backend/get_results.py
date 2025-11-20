import json
from utils import table, response
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """
    Query string params:
      exam_id (required)
      user_id (optional) -> to filter only that user's results
    """
    try:
        params = event.get("queryStringParameters") or {}
        exam_id = params.get("exam_id")
        user_id = params.get("user_id")

        if not exam_id:
            return response(400, {"error":"exam_id is required"})

        # fetch results
        pk = f"EXAM#{exam_id}"
        resp = table.query(KeyConditionExpression=Key("pk").eq(pk) & Key("sk").begins_with("RESULT#"), ScanIndexForward=False, Limit=100)

        items = resp.get("Items", [])
        if user_id:
            items = [i for i in items if i.get("user_id")==user_id]

        return response(200, {"results": items})
    except Exception as e:
        return response(500, {"error": str(e)})
