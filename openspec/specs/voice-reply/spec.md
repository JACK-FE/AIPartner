### Requirement: Voice toggle in chat header

聊天页头部 SHALL 显示语音播报开关按钮，用户可点击切换开启/关闭状态。

#### Scenario: Toggle appears when browser supports TTS
- **WHEN** 用户进入聊天页，且浏览器支持 `speechSynthesis`
- **THEN** 聊天页头部显示语音开关按钮

#### Scenario: Toggle hidden when browser does not support TTS
- **WHEN** 用户进入聊天页，且浏览器不支持 `speechSynthesis`
- **THEN** 聊天页头部不显示语音开关按钮

#### Scenario: Toggle on
- **WHEN** 用户点击关闭状态的语音开关
- **THEN** 开关切换为开启状态，后续 AI 回复将自动朗读

#### Scenario: Toggle off
- **WHEN** 用户点击开启状态的语音开关
- **THEN** 开关切换为关闭状态，正在播放的语音立即停止，后续 AI 回复不再朗读

### Requirement: Voice toggle state persistence

语音开关状态 SHALL 持久化到 localStorage，刷新页面后保持用户选择。

#### Scenario: State restored on page load
- **WHEN** 用户上次使用时开启了语音播报
- **THEN** 再次进入聊天页时，开关默认处于开启状态

#### Scenario: State persisted on toggle
- **WHEN** 用户切换语音开关
- **THEN** 新状态立即写入 localStorage

### Requirement: AI reply text-to-speech

AI 回复到达时，若语音已开启，系统 SHALL 在文字流式展示的同时朗读回复内容。

#### Scenario: Sentence-level playback during streaming
- **WHEN** AI 回复流式到达，且语音开关开启
- **THEN** 每遇到一个完整句子（以 。！？\n.!? 结尾）时，系统立即朗读该句子

#### Scenario: Remaining text played on stream end
- **WHEN** AI 回复流式结束（收到 done 事件）
- **THEN** 缓冲区中剩余未朗读的文本被一次性朗读

#### Scenario: No voice when toggle is off
- **WHEN** AI 回复到达，且语音开关关闭
- **THEN** 系统不触发任何语音播放，仅正常展示文字

### Requirement: Stop voice on new message

发送新消息时，系统 SHALL 停止当前正在播放的所有语音。

#### Scenario: New message interrupts current speech
- **WHEN** 用户发送新消息
- **THEN** 系统立即停止当前 AI 回复的语音播放，清空语音缓冲区

### Requirement: Stop voice on leave

离开聊天页时，系统 SHALL 停止语音播放。

#### Scenario: Voice stops when navigating away
- **WHEN** 用户从聊天页导航到其他页面
- **THEN** 所有进行中的语音播放被终止
