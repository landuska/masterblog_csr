from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post.", "category_id": 1},
    {"id": 2, "title": "Second post", "content": "This is the second post.", "category_id": 2},
    {"id": 3, "title": "Third post", "content": "This is the third post.", "category_id": 3},
    {"id": 4, "title": "Fourth post", "content": "This is the fourth post.", "category_id": 3}
]

CATEGORIES = [
    {"id": 1, "name": "Python"},
    {"id": 2, "name": "Weather"},
    {"id": 3, "name": "Restaurant"},
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


@app.route('/api/posts', methods=['POST'])
def create_posts():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is not provided"}), 400

    title = data.get("title")
    content = data.get("content")
    category_id = data.get("category_id")

    if not title or not content or not category_id:
        return jsonify({"error": "Title, content and  category_id are required"}), 400

    new_post = {
        "id": create_id(POSTS),
        "title": title,
        "content": content,
        "category_id": category_id
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


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


@app.route('/api/posts', methods=['GET'])
def get_sorted_posts():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    sort = request.args.get('sort', '').lower().strip()
    direction = request.args.get('direction', 'asc').lower().strip()

    results = list(POSTS)

    if sort:
        if sort not in ['title', 'content']:
            return jsonify({"error": f"Sort should be 'title' or 'content'."}), 400

        if direction not in ['asc', 'desc']:
            return jsonify({"error": f"Direction should be 'asc' or 'desc'."}), 400

        if direction == 'asc':
            results = sorted(results, key=lambda x: x[sort].lower(), reverse=False)
        else:
            results = sorted(results, key=lambda x: x[sort].lower(), reverse=True)

    start_index = (page - 1) * limit
    end_index = start_index + limit

    pagination_results = results[start_index:end_index]

    return jsonify(pagination_results), 200


@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(CATEGORIES), 200


@app.route('/api/posts/filter', methods=['GET'])
def filter_posts():
    category_input = request.args.get('category', '').strip()
    results = []

    if not category_input:
        return jsonify({"error": f"Category is required."}), 400

    for category in CATEGORIES:
        if category["name"].lower() == category_input.lower():
            results = [post for post in POSTS if post["category_id"] == category["id"]]

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
