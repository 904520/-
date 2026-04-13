# Backend API（第 1 阶段骨架）

## 启动方式
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 当前已实现接口
- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /memberships/plans`
- `POST /evidence/upload`
- `POST /drafts/generate`

## 说明
- 当前为启动骨架，数据存储为内存 + 本地文件，便于快速联调。
- 下一步建议接入 PostgreSQL、对象存储、支付系统与权限中间件。
