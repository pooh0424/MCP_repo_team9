# MCP Server + AI agent 分組實作

> 課程：AI Agent 開發 — MCP（Model Context Protocol）
> 主題：旅遊顧問 MCP Server (Theme A)

---

## Server 功能總覽

> 說明這個 MCP Server 提供哪些 Tool

| Tool 名稱               | 功能說明         | 負責組員 |
| ----------------------- | ---------------- | -------- |
| `get_weather`           | 查詢目的地天氣   | 呂紹銘   |
| `get_advice`            | 旅行前的人生建議 | 曹世杰   |
| `get_activity`	   | 推薦活動    | 林楷祐  |

---

## 組員與分工

| 姓名   | 負責功能             | 檔案                       | 使用的 API                        |
| ------ | -------------------- | -------------------------- | --------------------------------- |
| 呂紹銘 | 查詢目的地天氣       | `tools/weather_tool.py`    | `https://wttr.in/`                |
| 曹世杰 | 旅行前的人生建議     | `tools/get_advice_tool.py` | `https://api.adviceslip.com/advice`|
| 林楷祐 | 推薦活動   | `tools/get_activity_tool.py` |  https://bored-api.appbrewery.com/random   |
| 呂紹銘 | Resource + Prompt    | `server.py`                | —                                 |
| 呂紹銘 | Agent（用 AI 產生）  | `agent.py`                 | Gemini API                        |

---

## 專案架構

```
├── server.py              # MCP Server 主程式
├── agent.py               # MCP Client + Gemini Agent
├── tools/
│   ├── __init__.py
│   ├── weather_tool.py           # 呂紹銘的 Tool
│   ├── get_advice_tool.py        # 曹世杰的 Tool
│   └── get_adtivity_tool.py      # 林楷祐的 Tool
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 使用方式

```bash
# 1. 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定 API Key
cp .env.example .env
# 編輯 .env，填入你的 GEMINI_API_KEY

# 4. 用 MCP Inspector 測試 Server
mcp dev server.py

# 5. 用 Agent 對話
python agent.py
```

---

## 測試結果

### MCP Inspector 截圖

> 貼上 Inspector 的截圖（Tools / Resources / Prompts 三個分頁都要有）

### Agent 對話截圖

> 貼上 Agent 對話的截圖（顯示 Gemini 呼叫 Tool 的過程，以及使用 /use 呼叫 Prompt 的結果）

---

## 各 Tool 說明

### `get_weather`（負責：呂紹銘）

- **功能**：查詢目的地天氣
- **使用 API**：`https://wttr.in/{city}?format=j1`
- **參數**：`city` (字串，代表要查詢的城市名稱)
- **回傳範例**：

```text
📍 Taipei 目前天氣狀況：
☁️ 天氣：Light rain
🌡️ 溫度：21°C
💧 濕度：94%
💨 風速：14 km/h
```

```python
@mcp.tool()
def get_weather(city: str) -> str:
    """取得指定城市的即時天氣資訊。
    當使用者詢問天氣、溫度、是否該帶傘時使用。"""
    return get_weather_data(city)
```

### `get_advice`（負責：曹世杰）

- **功能**：旅行前的人生建議
- **使用 API**：https://api.adviceslip.com/advice
- **參數**：無
- **回傳範例**： If you're feeling tired or anxious, a pint of water will almost always make you feel better.

### `get_activity`（負責：林楷祐）

- **功能**：推薦活動
- **使用 API**：https://bored-api.appbrewery.com/random
- **參數**：無
- **回傳範例**：
```
推薦活動：Learn the Chinese erhu
可行性：0.4
活動類型：music
建議人數：1 人
花費：0.6
容易程度：Few to no challenges
活動時間：hours
適合小孩：是
活動編號：2742452
```

---

## 心得

### 遇到最難的問題

這次實作遇到比較困難的地方在於一開始要把 MCP Server 和 Agent 分開兩個終端機執行，並且理解它們之間 SSE (Server-Sent Events) 的連線與溝通機制。此外，在測試 Agent 呼叫 Gemini API 時，也遇到了 API Key 額度耗盡 (Quota Exceeded) 的狀況，後來透過去 Google AI Studio 申請新的 API Key 才順利完成測試。作為組長在整併大家開發的 Tools 到 `server.py` 時，也要特別注意 Git 的分支控管和合併衝突。

### MCP 跟上週的 Tool Calling 有什麼不同？

過去的 Tool Calling 通常需要把工具的程式碼邏輯跟 Agent (LLM) 的主程式綁死在一起，擴充與維護起來比較麻煩。而導入 MCP (Model Context Protocol) 後，最大的好處是「解耦（Decoupling）」。MCP Server 就像是一個獨立提供服務的載體（統一管理 Tools、Resources 和 Prompts），而 Agent 只要根據標準協議連上這個 Server，就可以自動「發現」並使用這些能力。這樣不僅讓程式碼架構更清晰，也做到一次開發能力即可給多個不同環境或 LLM Client 共用！
