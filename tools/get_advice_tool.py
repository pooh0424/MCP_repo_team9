

import requests

# Tool 資訊（給人看的，不影響 MCP）
TOOL_INFO = {
    "name": "get_advice",
    "api": "https://api.adviceslip.com/advice",
    "author": "曹世杰",
}

def get_advice() -> str:
    """呼叫 Advice Slip API，回傳一則旅行前的人生建議"""
    resp = requests.get("https://api.adviceslip.com/advice", timeout=10)
    resp.raise_for_status()
    return resp.json()["slip"]["advice"]


# 單獨測試
if __name__ == "__main__":
    print(get_advice())
