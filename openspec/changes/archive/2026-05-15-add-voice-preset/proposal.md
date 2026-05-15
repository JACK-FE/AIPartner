## Why

当前所有 AI 好友的语音播报听起来完全一样（浏览器默认中文语音），与角色的人格设定脱节。一个设定为「低沉稳重的大叔」和一个「元气活泼的少女」说出的话是同一个声音，这严重削弱了角色代入感和对话体验的真实性。

创建 AI 好友时设置音色，让每个角色拥有自己的声音身份，是角色人格完整性的核心一环。

## What Changes

- **AICharacter 模型新增 `voice_preset` 字段**，存储用户创建时选择的音色预设
- **TTS 引擎从浏览器端迁移到后端**：引入 Edge TTS（微软神经语音，完全免费），替代浏览器 `SpeechSynthesis`
- **定义 8 种中文音色预设**（少女音 / 活泼少女 / 东北女声 / 陕西女声 / 少年音 / 大叔音 / 正太音 / 新闻男声），运行时动态匹配 Edge TTS 可用语音
- **创建表单新增音色选择区**：预设卡片 + 试听按钮，交互参考现有头像选择
- **聊天页语音播放重构**：从 `speechSynthesis.speak()` 改为请求后端 TTS 接口获取音频并播放
- **TTS Provider 抽象层**：预留将来接入 Azure Speech / OpenAI TTS 等其他引擎的扩展点

## Capabilities

### New Capabilities
- `voice-preset`：AI 好友音色预设管理——预设定义、角色关联、后端 TTS 生成、试听预览

### Modified Capabilities
- `voice-reply`：语音播报引擎从浏览器 SpeechSynthesis 迁移到后端 Edge TTS，播放方式从直接朗读改为获取音频 URL 后播放

## Impact

- **后端改动**：AICharacter 模型新增字段 + 迁移；新建 `voice_presets.py`（预设定义）、`tts/` 模块（Provider 抽象 + Edge TTS 实现）；新增 TTS 和试听 API endpoint；Serializer 更新
- **前端改动**：`Create.vue` 新增音色选择区（预设卡片 + 试听）；`useVoice.ts` 重构（从 SpeechSynthesis 改为音频 URL 播放）；`Chat.vue` 播放逻辑适配
- **新增依赖**：`edge-tts`（Python 包，后端）
- **破坏性变更**：无（语音播报功能保持可用，仅更换底层实现）
