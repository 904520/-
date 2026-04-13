# Mobile App（Flutter）启动说明

当前仓库先完成 API 侧可联调骨架。移动端建议使用 Flutter 创建：

```bash
flutter create rights_guard_app
```

## 首批页面建议
1. 登录/注册页
2. 案件列表页
3. 材料上传页
4. 文书生成页（展示“分析摘要/风险提示/文书草稿”）
5. 会员中心页

## 接口联调建议
- Base URL: `http://<server>:8000`
- 先打通：注册 -> 登录 -> 上传材料 -> 生成投诉草稿
