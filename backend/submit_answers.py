import json
import uuid
from utils import table, response, iso_now
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """
    Expected event['body']:
    {
      "exam_id":"...",
      "user_id":"S001",
      "answers": [
         {"question_id":"q1","selected_option":2},
         ...
      ]
    }
    """
    try:
        body = json.loads(event.get("body") or "{}")
        exam_id = body["exam_id"]
        user_id = body["user_id"]
        answers = body.get("answers", [])

        # Fetch all questions for the exam to compute score
        resp = table.query(KeyConditionExpression=Key("pk").eq(f"EXAM#{exam_id}") & Key("sk").begins_with("QUESTION#"))
        questions = { item["sk"].split("QUESTION#")[1]: item for item in resp.get("Items", []) }

        total = 0
        correct = 0
        detailed = []
        for a in answers:
            qid = a["question_id"]
            selected = int(a["selected_option"])
            total += 1
            q = questions.get(qid)
            is_correct = False
            correct_opt = None
            if q:
                correct_opt = int(q.get("correct_option")) if q.get("correct_option") is not None else None
                if correct_opt is not None and selected == correct_opt:
                    correct += 1
                    is_correct = True
            detailed.append({"question_id": qid, "selected": selected, "correct_option": correct_opt, "is_correct": is_correct})

        score = int((correct / total) * 100) if total>0 else 0

        result_id = str(uuid.uuid4())
        result_item = {
            "pk": f"EXAM#{exam_id}",
            "sk": f"RESULT#{user_id}#{result_id}",
            "result_id": result_id,
            "user_id": user_id,
            "exam_id": exam_id,
            "score": score,
            "correct_count": correct,
            "total": total,
            "details": detailed,
            "submitted_at": iso_now()
        }
        table.put_item(Item=result_item)

        return response(200, {"message":"Submitted","score":score,"result_id":result_id})
    except KeyError as ke:
        return response(400, {"error":"Missing field: " + str(ke)})
    except Exception as e:
        return response(500, {"error": str(e)})
