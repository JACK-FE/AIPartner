# Tasks: fix-character-edit

## 1. Backend

- [x] 1.1 `AICharacterListSerializer` 的 `fields` 中添加 `"personality"` 和 `"model"` 字段
- [x] 1.2 验证 `/characters/mine/` 接口返回包含 `model` ID

## 2. Frontend — 编辑模式

- [x] 2.1 新增 `editingId` ref（`ref<number | null>(null)`）
- [x] 2.2 弹窗标题动态化：`:title="editingId ? '编辑AI好友' : '创建AI好友'"`
- [x] 2.3 提交按钮动态化：`{{ editingId ? '保存' : '创建' }}`
- [x] 2.4 创建卡片点击时重置 `editingId = null`
- [x] 2.5 `editCharacter()` 设置 `editingId = c.id`，正确回填所有字段（含 `model`）
- [x] 2.6 `handleCreate` 重构为 `handleSubmit`，分支调用 create/update API
- [x] 2.7 编辑成功后关闭弹窗、刷新列表、不重置表单

## 3. 验证

- [x] 3.1 创建新角色：标题"创建AI好友"、按钮"创建"、调用 POST
- [x] 3.2 编辑已有角色：标题"编辑AI好友"、按钮"保存"、表单完整回填
- [x] 3.3 编辑提交后调 PUT 而非 POST，角色被更新而非新增
- [x] 3.4 编辑成功后弹窗关闭、列表刷新
