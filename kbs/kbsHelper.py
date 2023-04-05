import os
import requests
import json
from models.api import QueryRequest, QueryResponse
from models.models import QueryResult, DocumentChunkWithScore


kbs_host = "https://lobster-app-r4gai.ondigitalocean.app"
upsert_url = kbs_host + "/upsert"
query_url = kbs_host + "/query"
kbs_token = os.environ.get("BEARER_TOKEN")

# Initialize the conversation history with a message from the chatbot
system_init_promote = "你将担任某个软件系统的客服助理。用户会问你一些使用此软件系统时遇到的问题。由于你并不非常了解此系统具体使用方法和程序模式，因此你需要借助一个知识库系统来回答用户的问题。你将分析用户的问题，生成对知识库系统的查询请求，然后把这个查询请求回复给用户。如果用户的提问中包含一个或多个具体问题，将每一个具体问题对应到使用特定查询关键字的query，每一个具体问题仅对应一个query. 同一问题只需生成一个query, 每一个query都要被包含在queries里面，并且只返回给用户一个queries实体。比如当用户问：”如何从SAP Ariba Procurement界面切换至Guided Buying，并创建采购项目“，你将回复json格式的查询请求，比如：{\"queries\": [ {\"query\": \"从SAP Ariba Procurement界面切换至Guided Buying\"}, {\"query\": \"在Guided Buying创建采购项目\"} ]}. 请注意，你仅仅只回复json格式的查询请求，你的回复中不能包含除了json实体以外的内容，如果没有需要查询知识库的内容，你将回复一个空格字符。"
init_message = {"role": "system", "content": system_init_promote}


kbs_ds = None


async def send_request(url, token, queries):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.post(url, headers=headers, json=queries)

    return response


def process_response(response_data):
    new_results = []
    print(f"original kbs response {response_data}")
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


def process_ds_response(ds_response):
    new_results = []
    for result in ds_response:
        query = result.query
        max_score_result = max(result.results, key=lambda x: x.score)

        if max_score_result.score > 0.8:
            new_result = {
                "query": query,
                "result": max_score_result.text
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


async def query_kbs(queries):
    if kbs_ds is None:
        response = await send_request(query_url, kbs_token, queries)

        if response.status_code == 200:
            return process_response(response.json())
        else:
            return f"Error: {response.status_code}"
    else:
        print("use kbs ds")
        query_request = QueryRequest(**queries)
        results = await kbs_ds.query(
            query_request.queries
        )

        return process_ds_response(results)
