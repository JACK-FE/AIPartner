"""
TTS Provider 抽象接口。
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseTTSProvider(ABC):
    """TTS 引擎的抽象基类。所有 TTS 实现必须继承此类。"""

    @abstractmethod
    async def synthesize(self, text: str, voice_id: str) -> bytes:
        """
        将文本合成为语音。

        Args:
            text: 要朗读的文本
            voice_id: TTS 引擎的 voice ID

        Returns:
            音频字节数据（MP3 格式）
        """
        ...

    @abstractmethod
    async def get_voice_list(self) -> List[Dict]:
        """
        获取该引擎支持的所有语音列表。

        Returns:
            list of dict，每个包含 name / gender / locale 等
        """
        ...
