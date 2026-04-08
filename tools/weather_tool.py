import requests

def get_weather_data(city: str) -> str:
    """取得指定城市的即時天氣資訊。"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data.get("current_condition", [{}])[0]
        
        status = current.get("lang_zh", [{}])[0].get("value", current.get("weatherDesc", [{}])[0].get("value", "未知"))
        temp_c = current.get("temp_C", "未知")
        humidity = current.get("humidity", "未知")
        wind_kph = current.get("windspeedKmph", "未知")
        
        return (
            f"📍 {city} 目前天氣狀況：\n"
            f"☁️ 天氣：{status}\n"
            f"🌡️ 溫度：{temp_c}°C\n"
            f"💧 濕度：{humidity}%\n"
            f"💨 風速：{wind_kph} km/h"
        )
    except Exception as e:
        return f"無法取得 {city} 的天氣資訊，錯誤：{str(e)}"
