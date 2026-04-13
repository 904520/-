# 02 系统架构（移动端 + AI 后端）

## 1. 总体架构
- 客户端：Flutter App（iOS/Android）
- API 网关：统一鉴权、限流、审计
- 业务后端：用户中心、会员中心、材料中心、文书中心
- AI 编排服务：检索、提取、推理、文书生成
- 数据层：PostgreSQL + 对象存储（S3 兼容）+ Redis

## 2. 核心服务模块
1) Auth Service
- 注册、登录、JWT/Refresh Token
- 设备管理、风控策略

2) Membership Service
- 订阅套餐、订单、权益校验
- 支付回调（微信/支付宝/应用内购）

3) Evidence Service
- 文件上传、OCR、ASR
- 材料标签、证据索引、时间线构建

4) Draft Service
- 文书模板管理
- AI 生成与多轮修订
- 导出 DOCX/PDF

5) Risk & Compliance Service
- 敏感词/违法用途拦截
- 法律免责声明注入
- 记录可审计日志

## 3. AI 流程（简化）
- Step A: 预处理（OCR/ASR/去噪/结构化）
- Step B: 事实抽取（人物、事件、证据引用）
- Step C: 冲突检测（时间矛盾、证据缺口）
- Step D: 文书生成（按模板与法条要点）
- Step E: 自检与提示（不确定项、需补证据）

## 4. 关键表设计（示例）
- users(id, phone, email, status, created_at)
- subscriptions(id, user_id, plan, expire_at, status)
- evidence_files(id, user_id, type, storage_key, parsed_text)
- cases(id, user_id, case_type, timeline_json, risk_level)
- drafts(id, case_id, doc_type, content, version)

## 5. 部署建议
- V1：单区域云部署（成本优先）
- V2：多可用区容灾 + 异地备份
- 监控：APM + 日志 + 告警（SLA/SLO 指标）
