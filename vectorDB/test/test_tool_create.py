import unittest
import os , sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from milvus_manager.milvus_manager import get_milvus_client
from tools.create import create_collection , gen_schema_format


class TestMilvusOperations(unittest.TestCase):
    def setUp(self):
        self.collection_name = "test_collection"
        self.schema = gen_schema_format()

    def test_create_collection(self):
        # Test creating a collection
        create_collection(self.collection_name, self.schema)
        client = get_milvus_client()
        self.assertTrue(client.has_collection(self.collection_name))

if __name__ == "__main__":
    unittest.main()