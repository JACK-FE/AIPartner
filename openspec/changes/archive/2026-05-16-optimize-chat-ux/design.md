# Design: optimize-chat-ux

## Architecture

改动涉及两个文件，不涉及后端。

```
Chat.vue
├── template
│   ├── 弹跳三点动画 (替换 <n-spin>)
│   ├── 快捷键切换按钮 (发送按钮旁，纯 span 实现)
│   ├── 聊天顶部简介 (替换模型名，n-ellipsis)
│   └── @keydown 事件处理
├── script
│   ├── sendOnEnter ref (localStorage 持久化)
│   ├── handleEnterKey / handleCtrlEnter
│   └── sendMessage() (TTS 保持原始全文合成)
└── style
    └── .typing-dots 动画 CSS

CharacterCard.vue
└── template
    └── n-ellipsis tooltip 宽度 + 方向
```

## 1. 打字指示器 — CSS 弹跳三点

```html
<span v-if="msg.id === 0 && !msg.content" class="typing-dots">
  <i>.</i><i>.</i><i>.</i>
</span>
```

```css
.typing-dots i {
  animation: dotBounce 1.4s infinite;
  font-style: normal;
}
.typing-dots i:nth-child(2) { animation-delay: 0.2s; }
.typing-dots i:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotBounce {
  0%, 80%, 100% { opacity: 0.2; transform: translateY(0); }
  40% { opacity: 1; transform: translateY(-3px); }
}
```

条件 `msg.id === 0 && !msg.content`：仅流式消息且尚未收到首 token 时显示，文字一到就消失。

## 2. 快捷键切换

**状态管理：**
```ts
const sendOnEnter = ref(localStorage.getItem('send_on_enter') !== 'false')
```

**键盘处理：**
```ts
function handleEnterKey(e: KeyboardEvent) {
  if (e.ctrlKey) return
  if (sendOnEnter.value) { e.preventDefault(); sendMessage() }
}

function handleCtrlEnter() {
  if (sendOnEnter.value) { inputText.value += '\n' }
  else { sendMessage() }
}
```

**UI 切换入口：**
使用纯 `<span>` 而非 `n-button`，避免 naive-ui 内部样式冲突导致蓝色 emoji：
```html
<span @click="toggleSendMode"
  style="color: #18a058; cursor: pointer; ..."
>{{ sendOnEnter ? '↩\uFE0E' : '⌃↩\uFE0E' }}</span>
```

关键点：
- `\uFE0E` (Variation Selector-15) 强制文字渲染，使 CSS `color: #18a058` 生效
- `height: 34px` 与发送按钮对齐
- hover 时浅绿背景 `#f0faf4`

## 3. 聊天顶部 — 简介替换模型名

```html
<n-ellipsis :line-clamp="1" :tooltip="{ style: { maxWidth: '300px' } }"
  style="font-size: 12px; color: #999; max-width: 300px;">
  {{ character.description || '暂无简介' }}
</n-ellipsis>
```

- `n-ellipsis` 自带 hover tooltip 显示全文
- `max-width: 300px` 限制显示和 tooltip 宽度

## 4. 广场卡片 tooltip 优化

```html
<n-ellipsis :line-clamp="2"
  :tooltip="{ style: { maxWidth: '280px' }, placement: 'bottom' }">
  {{ character.description || '暂无简介' }}
</n-ellipsis>
```

- `maxWidth: 280px` 防止 tooltip 过宽
- `placement: 'bottom'` 向下弹出，不遮挡上方头像

## 5. 流式语音（已回退）

Edge TTS 每次请求 1~3 秒网络延迟，无法做到文字语音真正同步。
并行请求方案导致音频播放顺序错乱。
恢复为原始行为：`finally` 块中获取完整 assistant 文本，调用 `ttsApi.synthesize` 全文合成。

## Key Decisions

| 决策 | 理由 |
|------|------|
| 纯 span 而非 n-button 做切换入口 | naive-ui quaternary button 内部样式使 emoji 强制蓝色，span 完全可控 |
| \uFE0E 变体选择符 | 强制文字渲染，CSS color 对 emoji 无效 |
| n-ellipsis 替代 CSS truncation | 自带 styled tooltip，体验优于原生 title |
| 流式语音回退 | Edge TTS 延迟无法消除，接受现实 |
