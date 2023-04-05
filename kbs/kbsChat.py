from kbs import kbsHelper
from kbs import gptAPIs
import json
import re


def parse_kbs_queries(response):
    # print(f"Find response: {response}")
    json_strings = re.findall(r'\{[^{}]*\}', response)
    results = []
    combined_queries = {"queries": results}
    for json_string in json_strings:
        json_obj = json.loads(json_string)
        if "query" in json_obj:
            results.append(json_obj)

    if len(results) > 0:
        return json.dumps(combined_queries, ensure_ascii=False)
    else:
        return ""


def generate_kbs_queries(user_input):
    kbs_message_log = [
        kbsHelper.init_message,
        {"role": "user", "content": "请对用户的提问内容：\"" + user_input + "\"进行分析，生成知识库查询请求"}
    ]

    # Send the conversation history to the chatbot and get its response
    response = gptAPIs.invoke_gpt(kbs_message_log)

    return parse_kbs_queries(response)


def generate_kbs_queries(user_input):
    kbs_message_log = [
        kbsHelper.init_message,
        {"role": "user", "content": "请对用户的提问内容：\"" + user_input + "\"进行分析，生成知识库查询请求"}
    ]

    # Send the conversation history to the chatbot and get its response
    response = gptAPIs.invoke_gpt(kbs_message_log)

    return parse_kbs_queries(response)


def format_kbs_queries(queries):
    format_text = ""
    if len(queries) > 0:
        queries_json = json.loads(queries)
        index = 0
        for result in queries_json["queries"]:
            index += 1
            query = result["query"]
            format_text += f"问题{index}: {query}\n"
    else:
        format_text = "无需使用知识库，请稍后\n"

    return format_text


async def chat_with_gpt(message_log, user_input, kbs_queries):
    if len(kbs_queries) > 0:
        print(f"use kbs queries {kbs_queries}")
        query_response = await kbsHelper.query_kbs(json.loads(kbs_queries))
        print(f"get kbs response {query_response}")
        query_response_json = json.loads(query_response)
        if len(query_response_json["results"]) > 0:
            user_input = user_input + "\n\n 你需要基于以下的知识来回答用户的问题: " + query_response
        else:
            print("no result from kbs")

    message_log.append({"role": "user", "content": user_input})
    # Send the conversation history to the chatbot and get its response
    response = gptAPIs.invoke_gpt(message_log)

    return response
