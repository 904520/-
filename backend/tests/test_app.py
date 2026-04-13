from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_register_login_and_generate_draft() -> None:
    register = client.post(
        "/auth/register",
        json={"phone": "13800000000", "password": "secret123"},
    )
    assert register.status_code == 200
    user_id = register.json()["user_id"]

    login = client.post(
        "/auth/login",
        json={"phone": "13800000000", "password": "secret123"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"].startswith("tk_")

    draft = client.post(
        "/drafts/generate",
        json={
            "user_id": user_id,
            "case_title": "拖欠工资",
            "case_type": "complaint",
            "facts": "2026年1月至3月，公司拖欠工资共计3万元，已多次催告未果，附聊天记录与考勤截图。",
            "claims": ["请求责令支付拖欠工资", "请求支付逾期利息"],
        },
    )
    assert draft.status_code == 200
    body = draft.json()
    assert "投诉举报材料" in body["document_title"]
    assert len(body["thinking_summary"]) >= 2
