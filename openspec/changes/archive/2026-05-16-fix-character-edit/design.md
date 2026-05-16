# Design: fix-character-edit

## Architecture

采用方案A — 在现有 `Create.vue` 中增加模式切换，不新建组件。

```
Create.vue
├── editingId: ref<number | null>    ← 新增：null=创建模式，非null=编辑模式
├── showCreateModal: ref<boolean>    ← 现有
├── form: ref<CreateForm>           ← 现有
├── openCreateModal()               ← 新增：重置为创建模式
├── editCharacter(c)                ← 修改：正确回填 model，设置 editingId
├── handleSubmit()                  ← 重构：拆分为创建/编辑两条路径
│   ├── 创建 → charactersApi.create()
│   └── 编辑 → charactersApi.update(editingId, data)
└── closeModal()                    ← 新增：关闭弹窗，编辑模式不重置表单
```

## Key Decisions

1. **用 `editingId` 而非独立页面** — 改动最小，表单字段完全相同，只有一个模式状态需要管理
2. **后端只改 serializer 不加接口** — `PUT /characters/{id}/` 已存在且完整，无需新增
3. **自定义头像按 data URI 继续上传** — 编辑模式下用户换头像时复用现有上传流程，不做特殊处理
4. **编辑成功后关闭弹窗不重置表单** — 表单状态随弹窗关闭自然销毁，下次打开时重新初始化

## Changes

### Backend: `serializers.py`

`AICharacterListSerializer.Meta.fields` 添加 `"personality"` 和 `"model"`：

```diff
 fields = (
     "id", "name", "avatar", "description", "is_public",
     "follow_count", "creator_name", "model_name",
-    "is_followed", "voice_preset", "created_at",
+    "is_followed", "voice_preset", "personality", "model", "created_at",
 )
```

### Frontend: `Create.vue`

核心改动：

1. 新增 `const editingId = ref<number | null>(null)`
2. 弹窗标题：`:title="editingId ? '编辑AI好友' : '创建AI好友'"`
3. 提交按钮：`{{ editingId ? '保存' : '创建' }}`
4. `editCharacter()`：设置 `editingId.value = c.id`，`form.value.model = c.model`
5. `handleCreate` 改名为 `handleSubmit`，按 `editingId` 分支调用不同 API
6. 创建卡片点击时：`editingId.value = null` 再打开弹窗
7. 取消/关闭时：重置 `editingId.value = null`

## Tradeoffs

| 方案 | 优点 | 缺点 |
|------|------|------|
| A: editingId 模式切换 | 改动小、复用高、快速交付 | 单文件逻辑略复杂 |
| B: 独立 Edit.vue | 代码清晰分离 | 大量重复、维护两套表单 |
| C: 路由参数 /create/:id? | URL 直观 | 需要路由改动、过度设计 |

当前表单字段少且创建/编辑完全一致，方案A是最合适的选择。
