import os , sys
import random

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if file_path not in sys.path:
    sys.path.append(file_path)

from tools.insert import insert_to_collection

mock_embedding = [random.uniform(-1.0, 1.0) for _ in range(1024)]
def test_insert_tool():
    assert insert_to_collection("test_collection",[{
        "text": "al",
        "embedding": mock_embedding,
        "source_file" : 'py10.2',
        "title": 'test',
        "chunk_index": 0,
        "metadata": {
            "source_file" : 'py10.2',
            "Title" : 'test'
        },
    }]) is True