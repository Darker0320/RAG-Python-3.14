from flask import Flask , request , jsonify
import re
import os, sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from vectorDB.tools.search import RAGRetriever
from RAG.generation.gen_context import generate_context , generate_new_prompt
from RAG.LLM.openai import send_request_to_openai

PATH_TRAVERSAL_PATTERN = re.compile(r'^(\.\./|\./|\.\.)')
app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/chat', methods=['POST'])
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
    search_results = retriever.hybrid_search(msg=message, hybrid_top_K=10, filter_expr="")
    if not search_results:
        return jsonify({"error": "No results found"}), 404

    rerank_doc = retriever.cross_rerank(query=message , candidates=search_results, top_k=5)
    generated_context = generate_context(rerank_doc=rerank_doc)
    generated_prompt = generate_new_prompt(user_message=message, context=generated_context)
    llm_message = send_request_to_openai(prompt=generated_prompt, tool="ollama")
    if llm_message['text'] == "":
        return jsonify({"error": "LLM returned empty response"}), 500

    return jsonify({"results": llm_message}), 200


if __name__ == '__main__':
    print("Starting Flask server on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)