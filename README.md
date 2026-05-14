# AI Partner

一个 AI 好友聊天社区平台。用户可以创建、定制 AI 虚拟角色，浏览公开角色，关注并与之聊天。

> [English Version](./README.en.md)

## 技术栈

- **前端**: Vue 3 + TypeScript + Naive UI + Pinia + Vue Router
- **后端**: Django + Django REST Framework + SimpleJWT
- **数据库**: SQLite（开发），可迁移至 MySQL

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

### 配置模型

访问 `http://localhost:8000/admin/` 登录超级管理员账号，在 Model Configs 中添加 LLM 模型配置（provider、model_name、api_key）。

## 页面

| 页面 | 路由 | 说明 |
|------|------|------|
| 广场 | `/` | 浏览公开 AI 角色，搜索、排序、筛选 |
| 聊天 | `/chat/:id` | 与 AI 角色实时流式对话 |
| 好友 | `/friends` | 最近聊天和关注的 AI 角色 |
| 创作 | `/create` | 创建和管理 AI 角色 |
| 个人 | `/profile` | 个人资料和头像管理 |
