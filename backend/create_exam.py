import json
import uuid
from utils import table, response, iso_now

def lambda_handler(event, context):
    """
    Expected event['body'] JSON:
    {
      "title": "Midterm 1",
      "exam_id": "optional; if not provided, generated",
      "date": "2025-11-20T10:00:00Z",
      "duration": 60,
      "questions": [
         {"question_id":"q1","question_text":"...","options":["a","b","c","d"],"correct_option":1}
      ]
    }
    """
    try:
        body = json.loads(event.get("body") or "{}")
        exam_id = body.get("exam_id") or str(uuid.uuid4())
        item = {
            "pk": f"EXAM#{exam_id}",
            "sk": "META",
            "exam_id": exam_id,
            "title": body.get("title","Untitled Exam"),
            "date": body.get("date"),
            "duration": int(body.get("duration", 60)),
            "created_at": iso_now()
        }
        # store questions as separate items with sk = QUESTION#<qid>
        table.put_item(Item=item)

        # questions
        questions = body.get("questions", [])
        for q in questions:
            q_item = {
                "pk": f"EXAM#{exam_id}",
                "sk": f"QUESTION#{q.get('question_id') or str(uuid.uuid4())}",
                "question_text": q.get("question_text"),
                "options": q.get("options", []),
                "correct_option": int(q.get("correct_option")) if q.get("correct_option") is not None else None
            }
            table.put_item(Item=q_item)

        return response(200, {"message":"Exam created","exam_id":exam_id})
    except Exception as e:
        return response(500, {"error": str(e)})
