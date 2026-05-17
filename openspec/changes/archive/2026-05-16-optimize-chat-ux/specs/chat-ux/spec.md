# Delta for chat-ux

## ADDED Requirements

### Requirement: 打字指示器动画
等待回复期间 MUST 显示弹跳三点动画，文字开始输出后消失。

#### Scenario: 发送消息后等待首 token
- GIVEN 用户刚发送了一条消息
- WHEN AI 尚未返回任何 token
- THEN 消息气泡内显示弹跳三点动画 "..."

#### Scenario: 首 token 到达后动画消失
- GIVEN AI 正在生成回复且尚未返回 token
- WHEN 第一个 token 到达
- THEN 三点动画立即消失
- AND 文字开始正常输出

### Requirement: 发送快捷键可切换
用户 MUST 能够在 Enter 发送和 Ctrl+Enter 发送之间切换。

#### Scenario: 默认 Enter 发送
- GIVEN 用户首次进入聊天界面
- WHEN 用户按下 Enter
- THEN 触发消息发送
- AND 按下 Ctrl+Enter 触发换行

#### Scenario: 切换为 Ctrl+Enter 发送
- GIVEN 用户点击快捷键切换按钮
- WHEN 按钮被点击
- THEN 模式切换为 Ctrl+Enter 发送 / Enter 换行
- AND 显示 toast 提示当前模式
- AND 偏好保存到 localStorage

#### Scenario: 重新进入时保持偏好
- GIVEN 用户之前切换为 Ctrl+Enter 发送模式
- WHEN 用户重新进入聊天界面
- THEN 快捷键模式保持为之前的选择

#### Scenario: 切换按钮配色统一
- GIVEN 页面主题色为绿色 #18a058
- WHEN 显示快捷键切换按钮
- THEN 按钮图标 MUST 显示为绿色而非默认蓝色
- AND 使用 text-presentation 变体避免 emoji 强制着色

### Requirement: 聊天顶部显示角色简介
聊天顶部角色名下方 MUST 显示角色简介而非模型名称。

#### Scenario: 简介过长时截断
- GIVEN 角色简介超过一行
- WHEN 显示在聊天顶部
- THEN 单行截断显示
- AND 鼠标悬停时弹出 tooltip 显示完整简介
- AND tooltip 宽度限制在 300px 以内

### Requirement: 广场卡片 tooltip 优化
广场角色卡片的简介 tooltip MUST 限制宽度且向下弹出。

#### Scenario: 悬停显示完整简介
- GIVEN 角色简介被截断
- WHEN 鼠标悬停在简介上
- THEN tooltip 在文本下方弹出
- AND tooltip 最大宽度限制为 280px
- AND 不遮挡上方头像
