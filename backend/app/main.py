from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

app = FastAPI(title="Rights Protection AI API", version="0.1.0")

DATA_DIR = Path(__file__).resolve().parent.parent / "storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class RegisterRequest(BaseModel):
    phone: str = Field(min_length=6, max_length=20)
    password: str = Field(min_length=6, max_length=64)


class LoginRequest(BaseModel):
    phone: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    expires_at: str


class MembershipPlan(BaseModel):
    code: Literal["free", "pro_month", "pro_year"]
    name: str
    monthly_quota: int


class DraftGenerateRequest(BaseModel):
    user_id: str
    case_title: str
    case_type: Literal["complaint", "reconsideration", "petition", "lawsuit"]
    facts: str = Field(min_length=20)
    claims: list[str]


class DraftGenerateResponse(BaseModel):
    draft_id: str
    document_title: str
    document_body: str
    thinking_summary: list[str]
    risk_notes: list[str]


USERS: dict[str, dict] = {}
TOKENS: dict[str, dict] = {}
EVIDENCE: dict[str, dict] = {}
DRAFTS: dict[str, dict] = {}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.post("/auth/register")
def register(payload: RegisterRequest) -> dict:
    if any(u["phone"] == payload.phone for u in USERS.values()):
        raise HTTPException(status_code=409, detail="phone already exists")

    user_id = f"u_{uuid4().hex[:10]}"
    USERS[user_id] = {
        "user_id": user_id,
        "phone": payload.phone,
        "password": payload.password,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "plan": "free",
    }
    return {"user_id": user_id, "plan": "free"}


@app.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    matched = next(
        (u for u in USERS.values() if u["phone"] == payload.phone and u["password"] == payload.password),
        None,
    )
    if not matched:
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = f"tk_{uuid4().hex}"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=12)
    TOKENS[token] = {"user_id": matched["user_id"], "expires_at": expires_at.isoformat()}
    return TokenResponse(access_token=token, expires_at=expires_at.isoformat())


@app.get("/memberships/plans", response_model=list[MembershipPlan])
def list_membership_plans() -> list[MembershipPlan]:
    return [
        MembershipPlan(code="free", name="免费版", monthly_quota=3),
        MembershipPlan(code="pro_month", name="会员月卡", monthly_quota=120),
        MembershipPlan(code="pro_year", name="会员年卡", monthly_quota=2000),
    ]


@app.post("/evidence/upload")
async def upload_evidence(
    user_id: str = Form(...),
    case_id: str = Form(...),
    file: UploadFile = File(...),
) -> dict:
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="user not found")

    suffix = Path(file.filename or "unknown.bin").suffix or ".bin"
    evidence_id = f"ev_{uuid4().hex[:12]}"
    local_path = DATA_DIR / f"{evidence_id}{suffix}"

    raw = await file.read()
    local_path.write_bytes(raw)

    item = {
        "evidence_id": evidence_id,
        "user_id": user_id,
        "case_id": case_id,
        "filename": file.filename,
        "size": len(raw),
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "storage_path": str(local_path),
    }
    EVIDENCE[evidence_id] = item
    return item


@app.post("/drafts/generate", response_model=DraftGenerateResponse)
def generate_draft(payload: DraftGenerateRequest) -> DraftGenerateResponse:
    if payload.user_id not in USERS:
        raise HTTPException(status_code=404, detail="user not found")

    header_map = {
        "complaint": "投诉举报材料",
        "reconsideration": "行政复议申请书",
        "petition": "信访材料",
        "lawsuit": "民事起诉状（草稿）",
    }
    doc_title = f"{header_map[payload.case_type]}：{payload.case_title}"
    claims_text = "\n".join([f"{idx + 1}. {c}" for idx, c in enumerate(payload.claims)])

    body = (
        f"一、基本事实\n{payload.facts}\n\n"
        "二、请求事项\n"
        f"{claims_text}\n\n"
        "三、证据说明\n"
        "（请在导出前补全证据编号、形成时间、来源与证明目的）\n"
    )

    thinking_summary = [
        "已提取争议主线并按事实->请求结构生成文书草稿。",
        "已保留证据补充占位，避免编造证据内容。",
        "建议补充关键时间节点与直接证据引用编号。",
    ]
    risk_notes = [
        "本草稿为法律信息辅助，不构成律师法律意见。",
        "请核验事实与证据一致性后再对外提交。",
    ]

    draft_id = f"dr_{uuid4().hex[:12]}"
    result = DraftGenerateResponse(
        draft_id=draft_id,
        document_title=doc_title,
        document_body=body,
        thinking_summary=thinking_summary,
        risk_notes=risk_notes,
    )
    DRAFTS[draft_id] = result.model_dump()
    return result
