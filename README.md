# 维权材料智能生成平台（启动版）

本仓库用于构建可在手机安装使用的“维权写材料”软件，核心能力包括：

- 用户上传证据材料（图片、PDF、录音转写、聊天记录等）
- 系统进行材料分析、证据链梳理与风险提示
- 自动生成多类文书：投诉举报材料、行政复议申请书、信访材料、起诉材料等
- 账号注册登录、会员订阅与权限控制
- 可解释的“思考能力”（展示推理步骤摘要，而非直接黑盒输出）

## 当前进展

### 第 0 阶段（已完成）
1. 明确产品边界与目标用户（见 `docs/01_product_scope.md`）
2. 输出系统架构与模块划分（见 `docs/02_architecture.md`）
3. 制定 12 周 MVP 落地计划（见 `docs/03_mvp_plan.md`）
4. 梳理合规与风控清单（见 `docs/04_compliance_risk.md`）

### 第 1 阶段（已启动）
- 已完成后端 API 骨架：注册登录、会员套餐、证据上传、文书草稿生成
- 已加入自动化测试（FastAPI TestClient）
- 已补充移动端 Flutter 启动与联调说明

## 快速开始（后端）
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 下一步
- 接入数据库（PostgreSQL）与对象存储（S3）
- 实现会员支付与权益校验闭环
- 增加证据抽取/OCR/ASR 编排与文书模板引擎
