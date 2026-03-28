from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def create_id(posts):
    """
    Generates a new unique ID based on the highest existing ID in the list.

    Args:
        posts (list): The current list of blog posts.

    Returns:
        int: The next available unique integer ID.
    """
    if not posts:
        return 1
    return max(int(post["id"]) for post in posts) + 1


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON data is not provided"}), 400

        title = data.get("title")
        content = data.get("content")

        if not title:
            return jsonify({"error": "Title is required"}), 400
        if not content:
            return jsonify({"error": "Content is required"}), 400

        new_post = {
            "id": create_id(POSTS),
            "title": title,
            "content": content
        }
        POSTS.append(new_post)

        return jsonify(new_post), 201

    elif request.method == 'GET':
        return jsonify(POSTS), 200


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def put(post_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is not provided"}), 400

    for post in POSTS:
        if post["id"] == post_id:
            post["title"] = data.get("title")
            post["content"] = data.get("content")
            return jsonify(post), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search():
    title_query = request.args.get("title")
    content_query = request.args.get("content")
    results = []

    for post in POSTS:
        title_match = title_query and title_query.lower() in post["title"].lower()
        content_match = content_query and content_query.lower() in post["content"].lower()

        if title_match or content_match:
            results.append(post)

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
