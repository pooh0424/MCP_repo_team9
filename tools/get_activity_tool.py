"""
Tool：取得隨機活動建議

這個 Tool 會呼叫 Bored API，
回傳一個適合旅途中參考的活動建議。
"""

import requests

# Tool 資訊（給人看的，不影響 MCP）
TOOL_INFO = {
    "name": "get_activity",
    "api": "https://bored-api.appbrewery.com/random",
    "author": "你的名字",
}


def get_activity_data() -> str:
    """呼叫 Bored API，回傳一個活動建議"""
    resp = requests.get("https://bored-api.appbrewery.com/random", timeout=10)
    resp.raise_for_status()
    data = resp.json()

    activity = data["activity"]
    availability = data["availability"]
    activity_type = data["type"]
    participants = data["participants"]
    price = data["price"]
    accessibility = data["accessibility"]
    duration = data["duration"]
    kid_friendly = "是" if data["kidFriendly"] else "否"
    link = data["link"]
    key = data["key"]

    result = (
        f"推薦活動：{activity}\n"
        f"可行性：{availability}\n"
        f"活動類型：{activity_type}\n"
        f"建議人數：{participants} 人\n"
        f"花費：{price}\n"
        f"容易程度：{accessibility}\n"
        f"活動時間：{duration}\n"
        f"適合小孩：{kid_friendly}\n"
        f"活動編號：{key}"
    )

    if link:
        result += f"\n參考連結：{link}"

    return result


# 單獨測試
if __name__ == "__main__":
    print(get_activity_data())
