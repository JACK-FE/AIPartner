"""
音色预设定义。

每个预设包含：
- key: 后端/数据库使用的标识符
- label: 前端展示的中文名称
- voice_id: Edge TTS 引擎的 voice ID
- gender: 性别（male / female）
- description: 声线描述
"""

VOICE_PRESETS = [
    {
        "key": "shaonv",
        "label": "少女音",
        "voice_id": "zh-CN-XiaoxiaoNeural",
        "gender": "female",
        "description": "年轻温柔，自然亲和",
    },
    {
        "key": "huopo",
        "label": "活泼少女",
        "voice_id": "zh-CN-XiaoyiNeural",
        "gender": "female",
        "description": "明快活泼，元气满满",
    },
    {
        "key": "dongbei",
        "label": "东北女声",
        "voice_id": "zh-CN-liaoning-XiaobeiNeural",
        "gender": "female",
        "description": "东北方言，爽朗亲切",
    },
    {
        "key": "shaanxi",
        "label": "陕西女声",
        "voice_id": "zh-CN-shaanxi-XiaoniNeural",
        "gender": "female",
        "description": "陕西方言，质朴温暖",
    },
    {
        "key": "shaonian",
        "label": "少年音",
        "voice_id": "zh-CN-YunxiNeural",
        "gender": "male",
        "description": "清爽阳光，青春洋溢",
    },
    {
        "key": "dashu",
        "label": "大叔音",
        "voice_id": "zh-CN-YunjianNeural",
        "gender": "male",
        "description": "低沉厚重，稳重成熟",
    },
    {
        "key": "zhengtai",
        "label": "正太音",
        "voice_id": "zh-CN-YunxiaNeural",
        "gender": "male",
        "description": "童稚可爱，纯真男孩",
    },
    {
        "key": "xinwen",
        "label": "新闻男声",
        "voice_id": "zh-CN-YunyangNeural",
        "gender": "male",
        "description": "专业播音，字正腔圆",
    },
]

PRESET_BY_KEY = {p["key"]: p for p in VOICE_PRESETS}
DEFAULT_PRESET_KEY = "shaonv"
