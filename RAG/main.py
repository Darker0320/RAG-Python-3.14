from flask import Flask , request , jsonify
import re
import os, sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from vectorDB.tools.search import RAGRetriever


PATH_TRAVERSAL_PATTERN = re.compile(r'^(\.\./|\./|\.\.)')
app = Flask(__name__)

def chatBox():
    if not request.method == 'POST':
        return jsonify({"error": "Invalid request method"}), 405
    request_data = request.get_json(silent=True)
    if request_data is None:
        return jsonify({
            "error": "Invalid or missing JSON data",
            "message": "Please ensure Content-Type is application/json and your JSON is valid."
        }), 400

    message = request_data.get('message')
    if PATH_TRAVERSAL_PATTERN.match(message):
        return jsonify({"error": "Path traversal detected"}), 400
    retriever = RAGRetriever(collection_name="python3_14",)
    search_results = retriever.search(msg=message, limit=10, filter_expr="")
    if not search_results:
        return jsonify({"error": "No results found"}), 404
    rerank_doc = retriever.rerank(msg=message , candidates=search_results, top_k=5 , min_score=0.15)

    return jsonify({"results": search_results}), 200

