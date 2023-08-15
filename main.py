import json

import weaviate

import re
def read_md(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 定义正则表达式模式
    title_pattern = r"^(# .+)"
    author_pattern = r">\s{2}(.+)"

    # 提取标题和作者
    title_match = re.search(title_pattern, text, re.MULTILINE)
    author_match = re.search(author_pattern, text, re.MULTILINE)

    if title_match and author_match:
        title = title_match.group(1)
        author = author_match.group(1)
        # 去除标题中的井号和空格
        title = title.replace("# ", "")
        # 提取内容部分
        content = text[author_match.end():].strip()
        content = content.replace("*", "").replace("#", "")
    result = {
        "title": title,
        "author": author,
        "content": content
    }
    return result
properties=[]
properties.append(read_md("data/test-dataset-1.md"))
properties.append(read_md("data/test-dataset-2.md"))
client = weaviate.Client(
    url="https://lcy-3koo0kfs.weaviate.network",  # Replace with your endpoint
    additional_headers={
            "X-HuggingFace-Api-Key": ""
        }
)

class_obj = {
  "class": "Article",
  "vectorizer": "text2vec-huggingface",
  "moduleConfig": {
    "text2vec-huggingface": {
      "model": "bert-base-chinese",
      "options": {
        "waitForModel": True,
      }
    }
  }
}
client.schema.delete_class(class_name='Article')
client.schema.create_class(class_obj)

with client.batch(
    batch_size=100
) as batch:
    # Batch import all Questions
    for i, d in enumerate(properties):
        print(f"importing data: {i+1}")

        properties = {
            "title": d["title"],
            "author": d["author"],
            "content": d["content"][0:490],
        }
        client.batch.add_data_object(
            properties,
            "Article",
        )

response = (
    client.query
    .aggregate("Article")
    .with_meta_count()
    .do()
)

print(json.dumps(response, indent=2))

