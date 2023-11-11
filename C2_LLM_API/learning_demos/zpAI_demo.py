import requests
import zhipuai
import time
import jwt
import os
from dotenv import load_dotenv, find_dotenv

# https://open.bigmodel.cn/dev/api#overview  智谱的接口文档
_ = load_dotenv(find_dotenv())
zp_api_key = os.environ["zp_api_key"]
print("* zp api key loaded")


# 使用 zhipuai 包的演示函数
def zhipuai_package_demo(key):
    # 设置zhipuai的api_key
    zhipuai.api_key = key

    # 使用zhipuai的model_api的invoke方法来调用模型并得到响应
    response = zhipuai.model_api.invoke(
        model="chatglm_turbo",
        prompt=[
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "我是人工智能助手"},
            {"role": "user", "content": "你叫什么名字"},
            {"role": "assistant", "content": "我叫chatGLM"},
            {"role": "user", "content": "你都可以做些什么事"},
        ],
        temperature=1,
    )
    print(response)


def zhipuai_package_demo_sse(key):
    # 设置zhipuai的api_key
    zhipuai.api_key = key

    # sse_invoke stream mode
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=[
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "我是人工智能助手"},
            {"role": "user", "content": "你叫什么名字"},
            {"role": "assistant", "content": "我叫chatGLM"},
            {"role": "user", "content": "请你用300字描述一下今天的心情"},
        ],
        temperature=0.9,
    )

    for event in response.events():
        if event.event == "add":
            # Print data continuously with controlled line breaks
            print(event.data, end="")
        elif event.event == "error" or event.event == "interrupted":
            print("\nError or Interrupted:", event.data)
        elif event.event == "finish":
            # Print any final data or meta information if needed
            print("\nFinished:", event.meta)
            break  # Break the loop once the generation is done
        else:
            print("\nOther Event:", event.data)


# 根据API密钥生成JWT令牌
def generate_token(api_key: str, exp_seconds: int):
    try:
        key, secret = api_key.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)
    payload = {
        "api_key": key,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,  # 过期时间
        "timestamp": int(round(time.time() * 1000)),  # 当前时间戳
    }
    # 使用 JWT 库编码并返回令牌
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


# 使用 requests 库调用 API 的演示函数
def requests_demo(key):
    model = "chatglm_lite"
    invoke_method = "invoke"
    url = f"https://open.bigmodel.cn/api/paas/v3/model-api/{model}/{invoke_method}"
    token = generate_token(key, 180)  # 生成JWT令牌
    response = requests.post(
        url=url,
        headers=dict(Authorization=token),  # 设置HTTP头部，包括JWT令牌
        json={
            "prompt": [
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "我是人工智能助手"},
                {"role": "user", "content": "你叫什么名字"},
                {"role": "assistant", "content": "我叫chatGLM"},
                {"role": "user", "content": "你都可以做些什么事"},
            ],
            "temperature": 1,
        },
    )
    print(response.json())


if __name__ == "__main__":
    zhipuai_package_demo_sse(zp_api_key)
