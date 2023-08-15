
import weaviate
import json
# 相似搜索
client = weaviate.Client(
    url="https://lcy-3koo0kfs.weaviate.network",  # Replace with your endpoint
    additional_headers={
            "X-HuggingFace-Api-Key": ""
        }
)
nearText = {"concepts": ["科技"]}

response = (
    client.query
    .get("Article", ["title", "author", "content"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=4,ensure_ascii=False))
exit()


# 关键字搜索
# where_filter = {
#   "path": ["title"],
#   "operator": "Like",
#   "valueText": "*科技*"
# }
#
# response = (
#   client.query
#   .get("Article", ["title", "author", "content"])
#   .with_where(where_filter)
#   .do()
# )
#
# print(json.dumps(response, indent=2,ensure_ascii=False))
