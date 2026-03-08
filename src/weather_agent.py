import requests


def query_weather(city: str) -> str:
    """
    查询指定城市的天气信息。
    :param city: 城市名称
    :return: 天气描述字符串
    """
    # 请替换为你自己的API_KEY
    API_KEY = "67732d7785c5436ebbd133704260803"
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=zh"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            weather = data["current"]["condition"]["text"]
            temp = data["current"]["temp_c"]
            return f"{city}当前天气：{weather}，温度：{temp}℃"
        else:
            return f"查询失败，状态码：{response.status_code}"
    except Exception as e:
        return f"查询异常：{e}"


if __name__ == "__main__":
    city = input("请输入城市名：")
    result = query_weather(city)
    print(result)
