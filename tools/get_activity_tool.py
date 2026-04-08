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
    try:
        resp = requests.get("https://bored-api.appbrewery.com/random", timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 429:
            return "很抱歉，目前活動建議的伺服器人數過多（Error 429: Too Many Requests），請稍後再試。"
        return f"取得活動建議時發生錯誤：{str(e)}"
    except Exception as e:
        return f"取得活動建議時發生錯誤：{str(e)}"

    activity = data.get("activity", "未知活動")
    availability = data.get("availability", "未知")
    activity_type = data.get("type", "未知")
    participants = data.get("participants", "未知")
    price = data.get("price", "未知")
    accessibility = data.get("accessibility", "未知")
    duration = data.get("duration", "未知")
    kid_friendly = "是" if data.get("kidFriendly") else "否"
    link = data.get("link", "")
    key = data.get("key", "未知")

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
