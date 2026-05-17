# Tasks: optimize-chat-ux

## 1. 打字指示器

- [x] 1.1 删除 `<n-spin>` 组件及其 import
- [x] 1.2 添加弹跳三点 HTML 模板（条件 `msg.id === 0 && !msg.content`）
- [x] 1.3 添加 `.typing-dots` CSS 动画样式

## 2. 发送快捷键互换

- [x] 2.1 新增 `sendOnEnter` ref，从 localStorage 读取默认值
- [x] 2.2 替换 `@keyup.ctrl.enter` 为 `@keydown.enter` + `@keydown.ctrl.enter`
- [x] 2.3 实现 `handleEnterKey` 和 `handleCtrlEnter` 分流逻辑
- [x] 2.4 发送按钮旁添加切换入口（最终方案：纯 span + \uFE0E，避免蓝色 emoji）
- [x] 2.5 `toggleSendMode` 切换 + toast 提示 + localStorage 写入

## 3. 流式语音（已回退）

- [x] ~~3.1~~ Edge TTS 网络延迟 + 并行请求顺序错乱，全部回退。恢复为文字完成后全文 TTS。

## 4. UI 细节优化

- [x] 4.1 聊天顶部：模型名替换为角色简介（`n-ellipsis` 单行截断 + tooltip）
- [x] 4.2 广场卡片：tooltip `max-width: 280px` + `placement: 'bottom'`
- [x] 4.3 聊天简介 tooltip：限制宽度 300px
- [x] 4.4 快捷键按钮蒙层：纯 span + \uFE0E 文字模式渲染，绿色 #18a058
