from FlagEmbedding import  BGEM3FlagModel

bge_m3 = BGEM3FlagModel(
    model_name_or_path="BAAI/bge-m3",
    model_name="BAAI/bge-m3",
    use_fp16=True,
    device="cuda:0",
)

def do_embedding(enhanced_content:str)->tuple[list[float], dict[int, float]]:
    embedding = bge_m3.encode(
        sentences=enhanced_content,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=False,
    )
    dense = embedding['dense_vecs'].tolist()

    sparse = {
        int(token_id): float(weight)
        for token_id, weight in dict(embedding['lexical_weights']).items()

    }
    return dense, sparse