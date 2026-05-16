# Proposal: fix-character-edit

## Why

AI好友的编辑功能目前没有实装。编辑界面虽然复用了创建表单并预填了部分数据，但存在三个关键问题：

1. **模型信息丢失** — 编辑时无法回填角色关联的模型（因为后端列表接口不返回 model ID）
2. **创建/编辑无区分** — 弹窗标题始终是"创建AI好友"，按钮始终是"创建"
3. **编辑实际执行的是创建** — 点击按钮后调用的是 POST（创建）而非 PUT/PATCH（更新），导致新增一个角色而非修改现有角色

## What Changes

- **后端** — `AICharacterListSerializer` 添加 `model` 字段（FK ID），让前端能从列表数据中获取角色关联的模型
- **前端** — `Create.vue` 引入 `editingId` 模式切换，区分创建/编辑两种状态：动态标题、动态按钮文字、正确的 API 调用、编辑成功后不重置表单

## Scope

- In scope: 后端 serializer 加字段、前端 Create.vue 编辑模式逻辑
- Out of scope: 独立编辑页面、编辑时头像上传流程变更、后端 API 变更（API 已有完整的 PUT/PATCH 支持）
