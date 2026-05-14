## Context

当前 Chat.vue 通过 SSE 流式接收 LLM token，逐字渲染到消息气泡中。项目使用 Vue 3 + Naive UI + Pinia 状态管理，聊天页无任何设置开关。需在纯前端新增语音播报能力，不改动后端。

## Goals / Non-Goals

**Goals:**
- AI 回复文字正常流式展示的同时，浏览器朗读回复内容
- 聊天页头部提供语音开关，可自由切换
- 开关状态持久化到 localStorage
- 发送新消息时自动停止上一段语音
- 离开聊天页时停止语音播放

**Non-Goals:**
- 不支持用户消息的语音播报（只为 AI 回复朗读）
- 不支持自定义语音/语速/音调选择
- 不支持语音输入（STT）
- 不做后端 TTS 集成

## Decisions

### 1. TTS 引擎：Web Speech API

选用 `window.speechSynthesis`，不引入第三方 TTS 服务。

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| Web Speech API | 免费、零依赖、浏览器原生 | 音质依赖系统 | ✅ 选用 |
| OpenAI TTS | 音质好、可流式 | 需 API key、有成本、需后端改动 | ❌ |
| Edge TTS | 免费、音质好 | Python 库、需后端 | ❌ |

### 2. 播放策略：句子级边界触发

Token 到达时累积到缓冲区，遇到句子分隔符（`。！？\n!?.;`）时立即朗读当前句子。

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| 全文播放（done 后） | 音频完整流畅 | 延迟大、不像"同时播放" | ❌ |
| 句子级播放 | 延迟小、体感自然 | 需要缓冲区逻辑 | ✅ 选用 |
| Token 级播放 | 最实时 | 音频碎片化、SpeechSynthesis 不支持逐 token 流式 | ❌ |

### 3. 开关持久化：localStorage

不引入后端存储或新的 Pinia store。状态管理内聚在 `useVoice` composable 中。

### 4. stop 时机：发送新消息时 + 离开页面时

发送新消息时调用 `voice.stop()` 中断当前朗读并清空缓冲，避免新回复与旧语音重叠。`onUnmounted` 时也调用 `voice.stop()`。

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| SpeechSynthesis 浏览器兼容性不一（Safari 语音列表少、部分移动端无中文） | composable 内检测 `speechSynthesis` 可用性，不可用时开关不显示 |
| 句子分割按标点符号可能不准确（如数字中的小数点） | 只对中文标点和明确英文句尾符号分割；数字中的 `.` 不触发 |
| 长句可能导致语音队列堆积 | 使用 `cancel()` 停止旧语音后再 `speak()`；缓冲区有上限 |
| 中文语音在不同操作系统上质量差异大 | 这是 SpeechSynthesis 的固有限制，不在此次范围内解决 |
