import requests


def query_wikipedia(keyword: str, lang: str = "zh") -> str:
    """
    查询维基百科指定词条的简介。
    :param keyword: 词条名称
    :param lang: 语言代码，默认中文
    :return: 词条简介或提示信息
    """
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{keyword}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "extract" in data and data["extract"]:
                return data["extract"]
            else:
                return None
        else:
            return None
    except Exception:
        return None


def query_qianwen(keyword: str) -> str:
    # 伪代码：请替换为你自己的千问API调用方式和API_KEY
    API_URL = "https://api.qianwen.aliyun.com/v1/chat/completions"
    API_KEY = "YOUR_QIANWEN_API_KEY"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "qwen-turbo",
        "messages": [
            {"role": "system", "content": "你是一个知识问答助手。"},
            {"role": "user", "content": f"请简要介绍：{keyword}"},
        ],
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=data, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            # 具体字段请根据千问API文档调整
            return result["choices"][0]["message"]["content"]
        else:
            return "千问API查询失败。"
    except Exception as e:
        return f"千问API异常：{e}"


if __name__ == "__main__":
    keyword = input("请输入要查询的维基百科词条：")
    result = query_wikipedia(keyword)
    if result:
        print(result)
    else:
        print("未找到维基百科简介，尝试使用千问大模型：")
        print(query_qianwen(keyword))
