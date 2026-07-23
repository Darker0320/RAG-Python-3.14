
from typing import Any

def generate_context(rerank_doc:list[dict[str, Any]]):
    context_blocks = []
    for idx, doc in enumerate(rerank_doc):
        entity = doc['entity']
        text = entity.get('text',"")
        source_file = entity.get('source_file',"Unknown")
        title = entity.get('title',"")
        header_path = entity.get('header_path',"Unknown")
        block = f'''
            Document {idx}
            Title: {title}
            Section: {header_path}
            Source File: {source_file}
            context: {text}
        '''.strip()

        context_blocks.append(block)
        context_blocks.append("================================\n\n")
    return "\n".join(context_blocks)

def generate_new_prompt(user_message:str, context:str):
    prompt = f'''
    You are a helpful assistant specialized in Python documentation.

    Use only the provided context to answer the user's question.
    Do not make up APIs, behaviors, version changes, or examples that are not supported by the context.

    Answer rules:
    1. If the context fully answers the question, answer directly.
    2. If the context partially answers the question, answer only the supported part and clearly state what is not covered by the context.
    3. If the context does not contain relevant information, respond exactly with:
    "I don't know based on the provided context."
    4. If multiple context chunks conflict, mention the uncertainty.
    5. Cite the source_file and header_path when possible.

    Style:
    - Be clear and concise.
    - Prefer practical examples only when the context supports them.
    - Do not include hidden reasoning or analysis.
    - Return only the final answer.

    Context:
    {context}

    User's Question:
    {user_message}

    Answer:
    '''.strip()
    return prompt