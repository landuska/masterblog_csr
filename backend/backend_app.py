from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)
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

USERS = [{"user_id": 1, "username": "Landysh", "password": 123, "token": "655fb71f-e927-4bc1-b413-7942c09b9f34"}]


def create_id(lst):
    """
    Generates a new unique ID based on the highest existing ID in the list.

    Args:
       lst: The current list

    Returns:
        int: The next available unique integer ID.
    """
    if not lst:
        return 1
    return max(int(item["id"]) for item in lst) + 1


def authenticate():
    token = request.headers.get("Authorization")
    return token if token else None


@app.route('/api/v1/posts', methods=['POST'])
@limiter.limit("10/minute")
def create_posts():
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

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

    return jsonify(new_post, {"message": f"Post was created successfully"}), 201


@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
def put(post_id):
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is not provided"}), 400

    for post in POSTS:
        if post["id"] == post_id:
            post["title"] = data.get("title")
            post["content"] = data.get("content")
            return jsonify(post, {"message": "Post was updated successfully"}), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/v1/posts/search', methods=['GET'])
@limiter.limit("10/minute")
def search():
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    title_query = request.args.get("title")
    content_query = request.args.get("content")
    results = []

    for post in POSTS:
        title_match = title_query and title_query.lower() in post["title"].lower()
        content_match = content_query and content_query.lower() in post["content"].lower()

        if title_match or content_match:
            results.append(post)

    return jsonify(results), 200


@app.route('/api/v1/posts', methods=['GET'])
@limiter.limit("10/minute")
def get_sorted_posts():
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

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


@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    return jsonify(CATEGORIES), 200


@app.route('/api/v1/posts/filter', methods=['GET'])
@limiter.limit("10/minute")
def filter_posts():
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    category_input = request.args.get('category', '').strip()
    results = []

    if not category_input:
        return jsonify({"error": f"Category is required."}), 400

    for category in CATEGORIES:
        if category["name"].lower() == category_input.lower():
            results = [post for post in POSTS if post["category_id"] == category["id"]]

    return jsonify(results), 200


@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    username = data.get("username").strip()
    password = data.get("password").strip()

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    for user in USERS:
        if user["username"] == username:
            return jsonify({"error": "User already exists"}), 400

    new_user = {
        "user_id": create_id(USERS),
        "username": username,
        "password": password
    }

    USERS.append(new_user)

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/api/v1/login', methods=['POST'])
@limiter.limit("10/minute")
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    username = data.get("username")
    password = data.get("password")

    for user in USERS:
        if user["username"] == username and user["password"] == password:
            token = str(uuid.uuid4())
            user["token"] = token

            return jsonify({"message": "Login successful", "token": token}), 200

    return jsonify({"error": "Invalid username or password"}), 401


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
