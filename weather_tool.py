"""
简易天气查询工具
功能：输入城市名称，调用公开 API 获取实时天气信息并显示
技术点：HTTP 请求、JSON 解析、异常处理、命令行交互
"""

import requests
import json
import sys

def get_weather(city_name):
    """
    查询指定城市的天气信息
    参数 city_name：城市名（支持中文）
    返回：格式化的天气信息字符串，查询失败返回 None
    """
    
    # 使用 wttr.in 提供的免费天气 API，无需注册密钥
    url = f"https://wttr.in/{city_name}?format=j1&lang=zh"
    
    try:
        # 发送 HTTP 请求，设置超时时间防止长时间等待
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析返回的 JSON 数据
        data = response.json()
        current = data['current_condition'][0]
        
        # 提取关键天气信息
        weather_info = {
            '城市': city_name,
            '温度': f"{current['temp_C']}°C",
            '体感温度': f"{current['FeelsLikeC']}°C",
            '天气': current['weatherDesc'][0]['value'],
            '湿度': current['humidity'],
            '风速': f"{current['windspeedKmph']} km/h",
            '风向': current['winddir16Point'],
            '能见度': f"{current['visibility']} km"
        }
        
        return weather_info
        
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接后重试")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到天气服务，请检查网络")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ 服务返回错误：{e}")
        return None
    except (KeyError, json.JSONDecodeError):
        print(f"❌ 未找到城市「{city_name}」的天气信息，请检查城市名称")
        return None
    except Exception as e:
        print(f"❌ 发生未知错误：{e}")
        return None


def display_weather(weather_info):
    """
    将天气信息格式化输出到控制台
    参数 weather_info：get_weather() 返回的字典
    """
    if weather_info is None:
        return
    
    print("\\n" + "=" * 40)
    print(f"🌍 {weather_info['城市']} 实时天气")
    print("=" * 40)
    print(f"🌡️  温度：{weather_info['温度']}（体感 {weather_info['体感温度']}）")
    print(f"☁️  天气：{weather_info['天气']}")
    print(f"💧 湿度：{weather_info['湿度']}")
    print(f"💨 风速：{weather_info['风速']}（风向：{weather_info['风向']}）")
    print(f"👁️  能见度：{weather_info['能见度']}")
    print("=" * 40 + "\\n")


def main():
    """
    主函数：处理命令行参数和交互循环
    """
    print("🌤️  欢迎使用简易天气查询工具")
    print("输入城市名查询天气，输入 'quit' 退出\\n")
    
    while True:
        try:
            city = input("请输入城市名称 > ").strip()
            
            if city.lower() == 'quit':
                print("👋 感谢使用，再见！")
                break
                
            if not city:
                print("⚠️  城市名不能为空，请重新输入\\n")
                continue
            
            # 查询并显示天气
            weather = get_weather(city)
            if weather:
                display_weather(weather)
                
        except KeyboardInterrupt:
            print("\\n\\n👋 检测到退出指令，再见！")
            break


if __name__ == "__main__":
    # 程序入口
    main()
