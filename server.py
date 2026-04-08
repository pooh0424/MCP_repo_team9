"""
W8 分組實作：MCP Server
主題：旅遊顧問 MCP Server (Theme A)

分工說明：
- 組長 呂紹銘
- 各組員在 tools/ 建立自己的 Tool，import 到這裡用 @mcp.tool() 註冊
- 指定一位組員負責 @mcp.resource()
- 指定一位組員負責 @mcp.prompt()
"""

from mcp.server.fastmcp import FastMCP
from tools.weather_tool import get_weather_data

mcp = FastMCP("旅遊顧問-server")


# ════════════════════════════════
#  Tools：各組員各自負責一個 Tool
# ════════════════════════════════

@mcp.tool()
def get_weather(city: str) -> str:
    """取得指定城市的即時天氣資訊。
    當使用者詢問天氣、溫度、是否該帶傘時使用。"""
    return get_weather_data(city)

@mcp.tool()
def hello(name: str) -> str:
    """跟使用者打招呼。測試用，確認 MCP Server 正常運作。"""
    return f"你好，{name}！MCP Server 運作正常 🎉"


# ════════════════════════════════
#  Resource：提供靜態參考資料
#  URI 格式：info://名稱 或 docs://名稱
# ════════════════════════════════

@mcp.resource("info://travel-tips")
def get_travel_tips() -> str:
    """旅行必帶物品與注意事項清單"""
    return (
        "旅行必帶物品：\n"
        "- 護照 / 身分證\n"
        "- 當地貨幣或信用卡\n"
        "- 備用藥品\n"
        "- 充電器與轉接頭\n\n"
        "出發前注意：\n"
        "- 確認當地天氣，準備適當衣物\n"
        "- 查詢當地緊急電話\n"
        "- 備份重要文件"
    )

# ════════════════════════════════
#  Prompt：提供大語言模型任務提示詞
# ════════════════════════════════

@mcp.prompt()
def plan_trip(city: str) -> str:
    """產生旅遊行前簡報的提示詞"""
    return (
        f"我要去 {city} 旅行，請幫我準備一份完整的行前簡報：\n"
        f"1. 查詢 {city} 的天氣，判斷需要帶什麼衣物\n"
        f"2. 給我一則旅遊相關的冷知識或趣味資訊\n"
        f"3. 給我一則旅行前的人生建議\n"
        f"4. 推薦 2-3 個在 {city} 可以做的活動\n"
        f"請用繁體中文，語氣活潑。"
    )

#     )


# ════════════════════════════════
#  Prompt：整合多個 Tool 的提示詞模板
#  使用者透過 /use <名稱> [參數] 呼叫
# ════════════════════════════════

# 範例（替換成符合你們主題的內容）：
#
# @mcp.prompt()
# def my_plan(topic: str) -> str:
#     """產生（主題）計畫的提示詞"""
#     return (
#         f"請幫我規劃關於 {topic} 的計畫：\n"
#         f"1. 先使用相關工具取得資訊\n"
#         f"2. 根據資訊提供 3 個具體建議\n"
#         f"3. 附上一則笑話或建議讓我開心\n"
#         f"請用繁體中文回答。"
#     )


if __name__ == "__main__":
    print("MCP Server 啟動中... http://localhost:8000")
    mcp.run(transport="sse")
