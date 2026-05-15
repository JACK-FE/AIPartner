## 1. Voice Preset Definitions (Backend)

- [x] 1.1 新建 `backend/apps/characters/voice_presets.py`，定义 `VOICE_PRESETS` 列表（8 种预设，包含 key / label / voice_id / gender / description）
- [x] 1.2 新建 `backend/apps/characters/tts/` 模块目录及 `__init__.py`

## 2. TTS Provider Abstraction

- [x] 2.1 新建 `backend/apps/characters/tts/base.py`，定义 `BaseTTSProvider` 抽象类
- [x] 2.2 新建 `backend/apps/characters/tts/edge_tts.py`，实现 `EdgeTTSProvider`，运行时动态获取可用语音列表并按关键词+性别做最佳匹配
- [x] 2.3 在 `requirements.txt` 中添加 `edge-tts>=7.2,<8.0` 依赖

## 3. AICharacter Model Update

- [x] 3.1 `AICharacter` 模型新增 `voice_preset` 字段（`CharField, max_length=32, default='shaonv'`）
- [x] 3.2 生成并运行数据库迁移

## 4. TTS API Endpoints

- [x] 4.1 新建 `POST /api/characters/{id}/tts/` 端点
- [x] 4.2 新建 `POST /api/tts/preview/` 端点
- [x] 4.3 TTS 生成的 MP3 文件存入 `MEDIA_ROOT/tts/`，按 `{timestamp}_{hash}.mp3` 命名
- [x] 4.4 TTS 文件定期清理（每次合成时删除超过 24 小时的文件）

## 5. Serializer Update

- [x] 5.1 `AICharacterCreateSerializer` 新增 `voice_preset`
- [x] 5.2 `AICharacterDetailSerializer` 返回 `voice_preset`、`voice_label`、`voice_id`
- [x] 5.3 `AICharacterListSerializer` 返回 `voice_preset`

## 6. Frontend Types & Constants

- [x] 6.1 `types/index.ts` 中 `AICharacter` 接口新增 `voice_preset` 等字段
- [x] 6.2 新建 `frontend/src/constants/voicePresets.ts`（8 种预设）

## 7. Create Form Voice Preset Selection

- [x] 7.1 在 `Create.vue` 表单中新增「音色」选择区，预设卡片 grid 展示
- [x] 7.2 选中态：绿色边框高亮，默认选中「少女音」
- [x] 7.3 表单提交包含 `voice_preset` 字段
- [x] 7.4 编辑预填：从已有数据恢复音色选中态

## 8. Trial Listening in Create Form

- [x] 8.1 每个音色卡片底部添加试听按钮
- [x] 8.2 点击试听按钮调用 `POST /api/tts/preview/`
- [x] 8.3 试听按钮加载态
- [x] 8.4 试听按钮 1 秒防抖

## 9. Refactor useVoice.ts

- [x] 9.1 移除 `SpeechSynthesis` 相关代码
- [x] 9.2 新增 `playAudio(url)` 方法
- [x] 9.3 `stop()` 改为停止当前 `<audio>` 播放
- [x] 9.4 移除 `feedToken` / `flush` 方法
- [x] 9.5 移除 `SENTENCE_END` 正则和 `buffer` 逻辑

## 10. Chat Page Voice Playback Update

- [x] 10.1 SSE 流结束后调用 TTS API 获取音频 URL
- [x] 10.2 使用 `voice.playAudio(url)` 播放
- [x] 10.3 发送新消息时调用 `voice.stop()`
- [x] 10.4 `onUnmounted` 时调用 `voice.stop()`
- [x] 10.5 移除 `voice.feedToken()` 调用

## 11. API Client Update

- [x] 11.1 `api/characters.ts` 中 `create` 方法参数新增 `voice_preset`
- [x] 11.2 新增 `ttsApi` 模块

## 12. Python 3.14 Compatibility

- [x] 12.1 新建 `config/py314_patch.py`，修复 Django 5.0 `BaseContext.__copy__()` 与 Python 3.14 不兼容问题
- [x] 12.2 在 `manage.py` 和 `wsgi.py` 中导入补丁
