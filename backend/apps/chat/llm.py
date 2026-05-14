import json
import urllib.request
from urllib.error import URLError


def stream_chat(model_config, messages):
    """Call OpenAI-compatible API and yield tokens."""
    api_key = model_config.api_key
    base_url = model_config.api_base_url or "https://api.openai.com/v1"
    model_name = model_config.model_name

    url = f"{base_url.rstrip('/')}/chat/completions"
    body = json.dumps({
        "model": model_name,
        "messages": messages,
        "stream": True,
    }).encode()

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req, timeout=60)
        for line in resp:
            line = line.decode("utf-8", errors="replace").strip()
            if not line or line.startswith("data: [DONE]"):
                continue
            if line.startswith("data: "):
                data = json.loads(line[6:])
                delta = data.get("choices", [{}])[0].get("delta", {})
                token = delta.get("content", "")
                if token:
                    yield token
    except URLError as e:
        yield f"\n\n[API Error: {e.reason}]"
    except json.JSONDecodeError:
        yield "\n\n[API Error: Failed to parse response]"
    except Exception as e:
        yield f"\n\n[API Error: {str(e)}]"
