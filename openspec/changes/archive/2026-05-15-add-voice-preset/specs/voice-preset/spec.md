## Requirements

### Requirement: Voice preset definition

系统 SHALL 预定义一组音色预设，每个预设包含唯一标识 key、中文名称 label、TTS 引擎 voice_id、性别 gender、声线描述 description。

#### Scenario: Preset list is available
- **WHEN** 系统启动
- **THEN** 8 种音色预设可被后端和前端引用，包括：少女音(shaonv)、活泼少女(huopo)、东北女声(dongbei)、陕西女声(shaanxi)、少年音(shaonian)、大叔音(dashu)、正太音(zhengtai)、新闻男声(xinwen)

#### Scenario: Preset maps to TTS voice ID
- **WHEN** 系统需要为预设「少女音」生成语音
- **THEN** 映射为 Edge TTS voice ID `zh-CN-XiaoxiaoNeural`

### Requirement: Voice preset on AI character

AICharacter 模型 SHALL 包含 `voice_preset` 字段，存储角色关联的音色预设 key，默认为 `shaonv`（少女音）。

#### Scenario: Character created with voice preset
- **WHEN** 用户创建 AI 好友时选择了「大叔音」
- **THEN** 角色的 `voice_preset` 字段值为 `dashu`

#### Scenario: Character created without voice preset
- **WHEN** 用户创建 AI 好友时未选择音色
- **THEN** 角色的 `voice_preset` 字段默认值为 `shaonv`

#### Scenario: Voice preset persisted and returned
- **WHEN** 查询角色详情或列表
- **THEN** API 响应中包含 `voice_preset` 字段及其对应的 label 和 voice_id

### Requirement: Voice preset selection in create form

创建 AI 好友的表单 SHALL 提供音色选择区域，以预设卡片形式展示所有可选音色，选中状态高亮。

#### Scenario: Voice preset cards displayed
- **WHEN** 用户打开创建 AI 好友的模态框
- **THEN** 表单中「音色」区域显示所有 8 种音色预设卡片，每张卡片显示预设名称和性别图标

#### Scenario: Preset selection with visual feedback
- **WHEN** 用户点击「大叔音」卡片
- **THEN** 该卡片显示绿色边框高亮（与头像选中样式一致），其他卡片恢复默认
- **AND** 表单数据中 `voice_preset` 值更新为 `dashu`

#### Scenario: Default preset selected
- **WHEN** 创建表单首次加载
- **THEN** 「少女音」卡片默认处于选中状态

### Requirement: Voice preset preview (trial listening)

创建表单中每个音色预设卡片 SHALL 提供试听按钮，点击后播放该音色的示例语音。

#### Scenario: Trial listening button on each card
- **WHEN** 用户在创建表单中查看音色选择区
- **THEN** 每个预设卡片上显示试听图标按钮

#### Scenario: Trial listening triggers audio playback
- **WHEN** 用户点击「大叔音」卡片的试听按钮
- **THEN** 前端请求 `POST /api/tts/preview/`，传入 `voice_preset: "dashu"` 和固定的试听文本
- **AND** 后端调用 Edge TTS 引擎生成音频，返回音频 URL
- **AND** 前端播放该音频

#### Scenario: Trial listening button debounced
- **WHEN** 用户在 1 秒内连续点击同一试听按钮
- **THEN** 仅触发一次试听请求

#### Scenario: Trial listening loading state
- **WHEN** 试听请求进行中
- **THEN** 试听按钮显示加载中状态，请求完成后恢复

### Requirement: Backend TTS synthesis with dynamic voice resolution

系统 SHALL 提供后端 TTS 合成能力，接收文本和音色预设 key，运行时从 Edge TTS 获取可用语音列表，动态匹配最佳 voice ID 后合成 MP3 音频。

#### Scenario: TTS synthesis for character
- **WHEN** 前端请求 `POST /api/characters/{id}/tts/`，传入 `{"text": "你好，最近过得怎么样？"}`
- **AND** 该角色的 `voice_preset` 为 `shaonian`
- **THEN** 后端动态匹配 `shaonian` → `zh-CN-YunxiNeural`
- **AND** 调用 Edge TTS 生成 MP3 音频文件保存到 `MEDIA_ROOT/tts/` 目录
- **AND** 返回 `{"audio_url": "/media/tts/{filename}.mp3"}`

#### Scenario: TTS synthesis with gender-based fallback
- **WHEN** 预设对应的 voice ID 在微软当前语音库中不存在
- **THEN** 系统按性别匹配同性别可用语音作为降级

#### Scenario: TTS synthesis for preview
- **WHEN** 前端请求 `POST /api/tts/preview/`，传入 `{"voice_preset": "dashu", "text": "你好，我是你的AI好友"}`
- **THEN** 后端动态匹配 `dashu` → `zh-CN-YunjianNeural`，生成 MP3 并返回 URL

#### Scenario: TTS synthesis failure handling
- **WHEN** Edge TTS 服务不可用或合成失败
- **THEN** 系统返回 502 状态码及错误详情，不崩溃

#### Scenario: TTS file cleanup
- **WHEN** 系统执行 TTS 合成
- **THEN** `MEDIA_ROOT/tts/` 目录中创建时间超过 24 小时的 MP3 文件被自动清理

### Requirement: Voice playback in chat

聊天页 AI 回复的语音播报 SHALL 使用后端 TTS 生成的音频，而非浏览器 SpeechSynthesis。

#### Scenario: AI reply voice playback
- **WHEN** AI 回复流式完成后，且语音开关开启
- **THEN** 前端请求 `POST /api/characters/{id}/tts/` 获取音频 URL
- **AND** 使用 `<audio>` 元素播放该音频

#### Scenario: Stop voice on new message
- **WHEN** 用户发送新消息时，当前有音频正在播放
- **THEN** 立即停止音频播放并释放资源

#### Scenario: No playback when voice toggle is off
- **WHEN** AI 回复完成，且语音开关关闭
- **THEN** 不请求 TTS 接口，不播放音频

### Requirement: TTS provider abstraction

后端 TTS 调用 SHALL 通过 Provider 抽象层实现，以便将来接入其他 TTS 引擎。

#### Scenario: Provider interface defined
- **WHEN** 查看 `tts/base.py`
- **THEN** 定义 `BaseTTSProvider` 抽象类，包含 `synthesize(text, voice_id) -> bytes` 和 `get_voice_list() -> list` 方法签名

#### Scenario: Edge TTS provider implemented
- **WHEN** 系统配置使用 Edge TTS
- **THEN** `EdgeTTSProvider` 实现 `synthesize` 方法，运行时动态获取可用语音列表并按关键词+性别做最佳匹配

#### Scenario: Provider configurable via settings
- **WHEN** 将来需要切换到 Azure Speech
- **THEN** 只需修改 Django settings 中的 TTS provider 配置并添加对应实现类，预设映射可复用
