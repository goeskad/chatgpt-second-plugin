import os
import requests
import json

kbs_host = "https://lobster-app-r4gai.ondigitalocean.app"
upsert_url = kbs_host + "/upsert"
query_url = kbs_host + "/query"
kbs_token = os.environ.get("BEARER_TOKEN")

# Initialize the conversation history with a message from the chatbot
system_init_promote = "你将担任某个软件系统的客服助理。用户会问你一些使用此软件系统时遇到的问题。由于你并不非常了解此系统具体使用方法和程序模式，因此你需要借助一个知识库系统来回答用户的问题。你将分析用户的问题，生成对知识库系统的查询请求，然后把这个查询请求回复给用户。如果用户的提问中包含一个或多个具体问题，将每一个具体问题对应到使用特定查询关键字的query，每一个具体问题仅对应一个query. 同一问题只需生成一个query。比如当用户问：”如何从SAP Ariba Procurement界面切换至Guided Buying，并创建采购项目“，你将回复json格式的查询请求，比如：{\"queries\": [ {\"query\": \"从SAP Ariba Procurement界面切换至Guided Buying\"}, {\"query\": \"在Guided Buying创建采购项目\"} ]}. 请注意，你只需回复json格式的查询请求，你永远都不应当尝试自己直接回答用户的问题。"
init_message = {"role": "system", "content": system_init_promote}


def send_request(url, token, queries):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.post(url, headers=headers, json=queries)

    return response


def process_response(response):
    response_data = response.json()
    new_results = []
    for result in response_data["results"]:
        query = result["query"]
        max_score_result = max(result["results"], key=lambda x: x["score"])

        if max_score_result["score"] > 0.8:
            new_result = {
                "query": query,
                "result": max_score_result["text"]
            }
            new_results.append(new_result)

    # 将处理后的结果输出为JSON格式
    output_data = {"results": new_results}
    output_json = json.dumps(output_data, ensure_ascii=False, indent=4)

    return output_json


def upsert_kbs(documents):
    documents_payload = {"documents": documents}
    response = send_request(upsert_url, kbs_token, documents_payload)

    if response.status_code == 200:
        return len(documents)
    else:
        return f"Error: {response.status_code}"


def query_kbs(queries):
    response = send_request(query_url, kbs_token, queries)

    if response.status_code == 200:
        return process_response(response)
    else:
        return f"Error: {response.status_code}"
