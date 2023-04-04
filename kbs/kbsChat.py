import kbsHelper
import gptAPIs
import json


def parse_kbs_queries(response):
    # print(f"Find response: {response}")
    json_text = ""
    start = response.find('{"queries')
    if start >= 0:
        json_text = response[start:]
        # 找到JSON内容的结束位置
        end = json_text.rfind(']}')
        if end > 0:
            # 保留JSON内容，去掉结束标记之后的部分
            json_text = json_text[:end+2]
            # print(f"Find queries: {json_text}")
            # queries = json.loads(json_text)

    return json_text


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


def chat_with_gpt(message_log, user_input, kbs_queries):
    if len(kbs_queries) > 0:
        print(f"use kbs queries {kbs_queries}")
        query_response = kbsHelper.query_kbs(json.loads(kbs_queries))
        query_response_json = json.loads(query_response)
        if len(query_response_json["results"]) > 0:
            user_input = user_input + "\n\n 你需要基于以下的知识来回答用户的问题: " + query_response
        else:
            print("no result from kbs")

    message_log.append({"role": "user", "content": user_input})
    # Send the conversation history to the chatbot and get its response
    response = gptAPIs.invoke_gpt(message_log)

    return response
