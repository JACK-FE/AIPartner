"""
Edge TTS Provider。

使用 edge-tts 库调用微软 Edge 在线 TTS 服务。
完全免费，无需 API Key。
"""

import io
from typing import List, Dict, Optional

import edge_tts

from .base import BaseTTSProvider

# 中文语音关键词匹配表：预设 key → 搜索关键词（在语音名中查找）
_VOICE_KEYWORDS: Dict[str, str] = {
    "shaonv": "Xiaoxiao",
    "huopo": "Xiaoyi",
    "dongbei": "Xiaobei",
    "shaanxi": "Xiaoni",
    "shaonian": "Yunxi",
    "dashu": "Yunjian",
    "zhengtai": "Yunxia",
    "xinwen": "Yunyang",
}


class EdgeTTSProvider(BaseTTSProvider):
    """Edge TTS 实现。运行时动态获取语音列表并匹配预设。"""

    def __init__(self):
        self._voice_id_cache: Optional[Dict[str, str]] = None

    async def _get_zh_voice_map(self) -> Dict[str, str]:
        """获取中文语音的 ShortName → Name 映射。"""
        if self._voice_id_cache is not None:
            return self._voice_id_cache

        try:
            voices = await edge_tts.list_voices()
        except Exception:
            print("[TTS] Failed to fetch voice list from Edge TTS")
            return {}

        zh_voices = [v for v in voices if v.get("Locale", "").startswith("zh-CN")]
        print(f"[TTS] Available zh-CN voices: {[v.get('ShortName') for v in zh_voices]}")

        # 按 ShortName 构建映射（优先精确匹配）
        voice_map: Dict[str, str] = {}
        for v in zh_voices:
            sn = v.get("ShortName", "")
            if sn:
                voice_map[sn] = sn

        self._voice_id_cache = voice_map
        return voice_map

    async def _resolve_voice_id(self, preset_key: str) -> str:
        """根据预设 key 解析实际的 voice ID。"""
        keyword = _VOICE_KEYWORDS.get(preset_key, "Xiaoxiao")

        # 尝试从运行时语音列表获取
        voice_map = await self._get_zh_voice_map()

        # 精确匹配
        candidate = f"zh-CN-{keyword}Neural"
        if candidate in voice_map:
            return candidate

        # 方言语音格式不同，特殊处理
        if not voice_map:
            return candidate

        # 关键词匹配
        for short_name in voice_map:
            if keyword.lower() in short_name.lower():
                return short_name

        # 降级：按性别匹配
        from ..voice_presets import PRESET_BY_KEY
        preset = PRESET_BY_KEY.get(preset_key, {})
        target_gender = preset.get("gender", "female")

        female_names = {"xiaoxiao", "xiaoyi", "xiaobei", "xiaoni"}
        male_names = {"yunxi", "yunjian", "yunxia", "yunyang"}

        same_gender = []
        for sn in voice_map:
            lower = sn.lower()
            if target_gender == "female" and any(fn in lower for fn in female_names):
                same_gender.append(sn)
            elif target_gender == "male" and any(mn in lower for mn in male_names):
                same_gender.append(sn)

        if same_gender:
            print(f"[TTS] Using same-gender fallback for '{preset_key}': {same_gender[0]}")
            return same_gender[0]

        print(f"[TTS] No match for '{preset_key}', using first available")
        return next(iter(voice_map.values()), candidate)

    async def synthesize(self, text: str, voice_id: str) -> bytes:
        """
        使用 Edge TTS 将文本合成为 MP3 音频。

        Args:
            text: 要朗读的文本
            voice_id: 可以是 ShortName（如 zh-CN-XiaoxiaoNeural）
                      或 preset key（如 shaonv）

        Returns:
            MP3 音频字节数据
        """
        # voice_id 可能是 preset key，解析为实际 voice ID
        resolved = voice_id
        if voice_id in _VOICE_KEYWORDS:
            resolved = await self._resolve_voice_id(voice_id)
        elif not voice_id.startswith("zh-CN-"):
            resolved = await self._resolve_voice_id(voice_id)

        print(f"[TTS] Synthesizing: preset={voice_id} voice={resolved} text_len={len(text)}")

        communicate = edge_tts.Communicate(text, resolved)
        buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buffer.write(chunk["data"])
        return buffer.getvalue()

    async def get_voice_list(self) -> List[Dict]:
        """
        获取 Edge TTS 可用语音列表。

        Returns:
            list of dict，包含 Name / Gender / Locale 等字段
        """
        voices = await edge_tts.list_voices()
        return [
            {
                "name": v["ShortName"],
                "gender": v["Gender"],
                "locale": v["Locale"],
            }
            for v in voices
        ]
