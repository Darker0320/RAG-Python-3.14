import os , sys
from pathlib import Path
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if file_path not in sys.path:
    sys.path.append(file_path)

from clean_doc.process_markdown import dismantle_begM3
from vectorDB.tools.create import create_collection , gen_schema_format , create_index
from vectorDB.tools.insert import insert_to_collection
from vectorDB.tools.load_collection import load_collection

collection_name = f"python3_14"
def main():
    cleaned_docs = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).joinpath('clean_doc', 'cleaned_docs')
    if not cleaned_docs.exists():
        print(f"file : {cleaned_docs} not exists, Please check the path.")
        return

    folders = sorted([d for d in cleaned_docs.iterdir() if d.is_dir()])
    if not folders:
        folders = [cleaned_docs]
    docs = []
    for folder in folders:
        txt_files = sorted(folder.rglob('*.md'))
        if not txt_files:
                continue
        for file_path in txt_files:
            docs.extend(dismantle_begM3(file_path))
    create_collection(collection_name, gen_schema_format())
    try:
        if insert_to_collection(collection_name, docs , batch_size=1000):
            if create_index(collection_name):
                if load_collection(collection_name):
                    print("success load collection to milvus")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()