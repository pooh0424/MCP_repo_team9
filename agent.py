import asyncio
import os
from dotenv import load_dotenv
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    print("❌ 請在 .env 檔案中設定 GEMINI_API_KEY")
    exit(1)

client = genai.Client(api_key=gemini_api_key)

async def run_agent():
    print("🔄 正在連接到 MCP Server (http://localhost:8000/sse)...")
    try:
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✅ 成功連接到 MCP Server！")

                # 1. 取得 Server 提供的所有工具
                tools_response = await session.list_tools()
                
                # 2. 將 MCP Tools 轉換為 Gemini Function Declarations
                gemini_tools = []
                for tool in tools_response.tools:
                    # 轉換 JSON Schema
                    props = {}
                    if tool.inputSchema and "properties" in tool.inputSchema:
                        for key, val in tool.inputSchema["properties"].items():
                            props[key] = types.Schema(
                                type=val.get("type", "STRING").upper(),
                                description=val.get("description", "")
                            )
                    
                    gemini_tools.append(
                        types.FunctionDeclaration(
                            name=tool.name,
                            description=tool.description,
                            parameters=types.Schema(
                                type=types.Type.OBJECT,
                                properties=props,
                                required=tool.inputSchema.get("required") if tool.inputSchema else None
                            )
                        )
                    )
                
                tool_config = types.Tool(function_declarations=gemini_tools)
                
                print(f"🛠️ 載入了 {len(gemini_tools)} 個工具")
                print("🤖 Gemini Agent 已啟動，請輸入您的問題 (輸入 'quit' 或 'exit' 離開)：")
                
                # 建立 Chat Session
                chat = client.chats.create(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        tools=[tool_config] if gemini_tools else None
                    )
                )

                while True:
                    try:
                        user_input = input("\n👤 User: ")
                    except EOFError:
                        break
                        
                    if user_input.lower() in ['quit', 'exit']:
                        print("👋 再見！")
                        break
                    if not user_input.strip():
                        continue

                    # 送出訊息給 Gemini
                    try:
                        response = chat.send_message(user_input)
                        
                        # 處理 function calls
                        while response.function_calls:
                            for function_call in response.function_calls:
                                tool_name = function_call.name
                                tool_args = {}
                                if function_call.args:
                                    for key, value in function_call.args.items():
                                        tool_args[key] = value
                                
                                print(f"  [Auto] 呼叫工具 🛠️: {tool_name}({tool_args})")
                                
                                # 透過 MCP 呼叫 Server 端工具
                                result = await session.call_tool(tool_name, arguments=tool_args)
                                
                                # 擷取結果文本
                                tool_text = "\n".join([c.text for c in result.content if getattr(c, 'type', '') == 'text'])
                                print(f"  [Auto] 工具結果 📄:\n{tool_text}")
                                
                                # 將結果回傳給 Gemini
                                response = chat.send_message(
                                    [types.Part.from_function_response(
                                        name=tool_name,
                                        response={"result": tool_text}
                                    )]
                                )
                        
                        # 顯示最終回答
                        if response.text:
                            print(f"\n🤖 Agent: {response.text}")
                            
                    except Exception as e:
                        print(f"❌ 處理過程中發生錯誤: {e}")
                        
    except Exception as e:
        print(f"❌ 無法連接到 MCP Server: {e}\n請確認您有先在另一個終端機執行 `python server.py`。")

if __name__ == "__main__":
    asyncio.run(run_agent())

