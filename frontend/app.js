// EDIT these endpoints after deploying your Lambdas
const API_BASE = "https://<YOUR_API_GATEWAY>.execute-api.<region>.amazonaws.com/dev";

document.getElementById("btnCreateExam").onclick = async () => {
  const payload = document.getElementById("examPayload").value;
  try {
    const res = await fetch(`${API_BASE}/exams/create`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: payload
    });
    const data = await res.json();
    document.getElementById("createResponse").innerText = JSON.stringify(data, null, 2);
  } catch (e) {
    document.getElementById("createResponse").innerText = e;
  }
};

document.getElementById("btnSubmitAnswers").onclick = async () => {
  const exam_id = document.getElementById("examIdInput").value;
  const user_id = document.getElementById("userIdInput").value || "S001";
  const answers = document.getElementById("answersPayload").value;
  try {
    const body = JSON.stringify({exam_id, user_id, answers: JSON.parse(answers)});
    const res = await fetch(`${API_BASE}/exams/submit`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body
    });
    const data = await res.json();
    document.getElementById("submitResponse").innerText = JSON.stringify(data, null, 2);
  } catch (e) {
    document.getElementById("submitResponse").innerText = e;
  }
};

document.getElementById("btnGetResults").onclick = async () => {
  const exam_id = document.getElementById("resultExamId").value;
  const user_id = document.getElementById("resultUserId").value;
  const qs = new URLSearchParams({exam_id});
  if (user_id) qs.append("user_id", user_id);
  try {
    const res = await fetch(`${API_BASE}/exams/results?${qs.toString()}`);
    const data = await res.json();
    document.getElementById("resultsPre").innerText = JSON.stringify(data, null, 2);
  } catch (e) {
    document.getElementById("resultsPre").innerText = e;
  }
};
