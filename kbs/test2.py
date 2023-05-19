import re
import json

s = '{"queries": [{"query": "如何注册新的供应商账号"}]} 针对第二个具体问题，可以生成如下查询请求： {"queries": [{"query": "如何更改订购单"}]}第三个是 {"jks": [{"query": "如何更改订购单"}]}'

# 使用正则表达式找到字符串中的所有JSON内容
json_strings = re.findall(r'\{[^{}]*\}', s)

combined_queries = {"queries": []}

for json_string in json_strings:
    json_obj = json.loads(json_string)
    if "query" in json_obj:
        combined_queries["queries"].append(json_obj)

# 将合并后的JSON对象转换为字符串
combined_json = json.dumps(combined_queries, ensure_ascii=False)

print(combined_json)
