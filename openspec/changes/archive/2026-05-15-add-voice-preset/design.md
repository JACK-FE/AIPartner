## Context

当前项目已实现语音播报（`voice-reply` spec），但使用浏览器 `SpeechSynthesis` API，无法控制音色。AICharacter 模型包含 name / avatar / description / personality / model 等字段，无音色相关字段。创建表单支持头像预设选择模式（缩略图点选），可作为音色选择的交互参考。

此次改动将 TTS 从浏览器端迁移到后端，引入 Edge TTS 引擎（微软神经语音，完全免费），同时在后端建模音色预设概念，使其成为 AI 角色的固有属性。

实现过程中，微软精简了 Edge TTS 的中文语音库（从 15+ 缩减到 8 种），最终采用运行时动态获取语音列表 + 关键词和性别降级匹配的策略，确保预设始终映射到实际可用的语音。

## Goals / Non-Goals

**Goals:**
- 创建 AI 好友时可选择音色预设（8 种：少女音 / 活泼少女 / 东北女声 / 陕西女声 / 少年音 / 大叔音 / 正太音 / 新闻男声）
- 每个预设试听功能（创建表单内点击试听按钮，播放预设短句）
- 聊天时 AI 回复使用角色设定的音色进行语音播报
- TTS 引擎替换为后端 Edge TTS，提供一致的跨设备语音体验
- TTS 调用抽象为 Provider 接口，预留扩展点
- 运行时动态匹配：微软增删语音时自动适配

**Non-Goals:**
- 不支持用户自行上传/训练自定义音色
- 不支持音色参数微调（语速、音调等）
- 不支持创建后修改音色（编辑功能复用创建表单，本次不额外开发）
- 不做流式逐句朗读（首版整段生成后一次性播放）
- 不支持语音输入（STT）

## Decisions

### 1. TTS 引擎：Edge TTS

选用 `edge-tts` Python 库，调用微软 Edge 在线 TTS 服务。与 Azure Speech 共享同一套神经语音模型，中文质量优秀。

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| Edge TTS | 完全免费、中文神经语音、零配置、即装即用 | 非官方接口 | ✅ 选用 |
| Azure Speech | 官方 API、SLA 保障、同款语音 | 需 Azure 账号+付费 | 后续升级路径 |
| OpenAI TTS | API 简洁 | 仅 6 种英文优化语音，中文差、贵 | ❌ |
| 浏览器 SpeechSynthesis | 零依赖 | 音色不可控、跨设备不一致 | ❌ 废弃 |

### 2. 音色预设映射（运行时动态）

原本设计为 14 种预设硬编码映射。实现时发现微软 2026 年大幅精简了中文语音库，仅保留 8 种。最终采用运行时动态匹配策略：

```
预设 key    →   关键词     →   运行时语音列表查找
shaonv      →   Xiaoxiao   →   zh-CN-XiaoxiaoNeural ✓ 精确匹配
dongbei     →   Xiaobei    →   zh-CN-XiaobeiNeural ✗ → zh-CN-liaoning-XiaobeiNeural ✓ 关键词匹配
(已移除)    →   Xiaoshuang →   ✗ 不在列表中 → 按性别降级到同性别可用语音
```

策略链：精确匹配 → 关键词匹配 → 按性别降级 → 兜底。

### 3. 最终 8 种预设

| key | label | 关键词 | 性别 | 声线描述 |
|-----|-------|--------|------|----------|
| shaonv | 少女音 | Xiaoxiao | 女 | 年轻温柔，自然亲和 |
| huopo | 活泼少女 | Xiaoyi | 女 | 明快活泼，元气满满 |
| dongbei | 东北女声 | Xiaobei | 女 | 东北方言，爽朗亲切 |
| shaanxi | 陕西女声 | Xiaoni | 女 | 陕西方言，质朴温暖 |
| shaonian | 少年音 | Yunxi | 男 | 清爽阳光，青春洋溢 |
| dashu | 大叔音 | Yunjian | 男 | 低沉厚重，稳重成熟 |
| zhengtai | 正太音 | Yunxia | 男 | 童稚可爱，纯真男孩 |
| xinwen | 新闻男声 | Yunyang | 男 | 专业播音，字正腔圆 |

### 4. 播放策略：整段生成，一次性播放（方案 A）

AI 回复流式到达时，前端正常展示文字。流结束后，后端用完整文本调用 TTS，返回音频 URL，前端播放。

### 5. TTS Provider 抽象层

```
backend/apps/characters/tts/
├── __init__.py
├── base.py           # 抽象接口
├── edge_tts.py       # Edge TTS 实现（含运行时语音匹配）
└── (future) azure.py / openai.py
```

### 6. API 设计

```
POST /api/characters/{id}/tts/   → 角色 TTS（聊天用）
POST /api/tts/preview/           → 试听预览（创建表单用）
```

生成的 MP3 文件存入 `MEDIA_ROOT/tts/`，按时间戳+hash 命名，每次合成时清理超过 24 小时的文件。

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|----------|
| Edge TTS 是非官方接口，可能被限流或封堵 | Provider 抽象层已预留切换点 |
| 微软随时可能增删语音 | 运行时动态匹配 + 性别降级策略 |
| 生成的 MP3 文件堆积占用磁盘 | 按时间戳命名，每次合成时清理 24 小时前的文件 |
| 试听功能可能被频繁请求 | 前端按钮 1 秒防抖 |
