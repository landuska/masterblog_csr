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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
