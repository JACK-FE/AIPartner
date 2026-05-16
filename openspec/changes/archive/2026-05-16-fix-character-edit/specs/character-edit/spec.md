# Delta for character-edit

## MODIFIED Requirements

### Requirement: AI好友列表接口返回模型ID和性格描述
后端 `/characters/mine/` 和 `/characters/` 列表接口的响应 MUST 包含 `model` 和 `personality` 字段，以便前端在编辑时回填模型选项和性格描述。

#### Scenario: 获取我的角色列表时包含模型ID
- GIVEN 用户已登录且有已创建的AI好友
- WHEN 调用 `GET /characters/mine/`
- THEN 返回的每个角色对象包含 `model: <integer>` 字段，值为关联的 ModelConfig ID

#### Scenario: 获取公开角色列表时包含模型ID
- GIVEN 存在公开的AI好友
- WHEN 调用 `GET /characters/`
- THEN 返回的每个角色对象包含 `model: <integer>` 字段

## ADDED Requirements

### Requirement: 编辑模式与创建模式区分
编辑AI好友时，表单 MUST 明确标识为编辑模式，与创建模式有视觉和行为的区分。

#### Scenario: 从角色卡片点击编辑按钮
- GIVEN 用户在看自己创建的AI好友列表
- WHEN 点击某个角色的"编辑"按钮
- THEN 弹窗标题显示"编辑AI好友"
- AND 表单预填该角色的所有已有信息（名称、头像、简介、性格、音色、模型、公开状态）
- AND 提交按钮显示"保存"

#### Scenario: 从创建卡片点击进入
- GIVEN 用户在看自己创建的AI好友列表
- WHEN 点击"+ 创建AI好友"卡片
- THEN 弹窗标题显示"创建AI好友"
- AND 表单为空（默认值）
- AND 提交按钮显示"创建"

### Requirement: 编辑提交调用更新接口
编辑模式下提交表单 MUST 调用 PUT 更新接口，而非 POST 创建接口。

#### Scenario: 编辑已有角色并保存
- GIVEN 用户在编辑模式下修改了某个角色的信息
- WHEN 点击"保存"按钮
- THEN 调用 `PUT /characters/{id}/` 接口
- AND 成功后显示"更新成功"提示
- AND 关闭弹窗
- AND 刷新角色列表
- AND 不重置表单（因为弹窗已关闭）

#### Scenario: 创建新角色
- GIVEN 用户在创建模式下填写了角色信息
- WHEN 点击"创建"按钮
- THEN 调用 `POST /characters/` 接口
- AND 行为与现有逻辑一致（成功提示、关闭弹窗、重置表单、刷新列表）
