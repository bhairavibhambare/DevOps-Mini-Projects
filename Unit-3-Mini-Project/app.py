from flask import Flask, jsonify, request

app = Flask(__name__)

books = {
    1: {"id": 1, "title": "Python Basics", "borrowed": False},
    2: {"id": 2, "title": "DevOps Fundamentals", "borrowed": False},
}


@app.get("/")
def home():
    return jsonify({
        "project": "Enterprise Smart Library Management Platform",
        "version": "v1.0.0",
        "status": "running"
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/books")
def list_books():
    return jsonify(list(books.values()))


@app.post("/books")
def add_book():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    book_id = max(books.keys(), default=0) + 1
    books[book_id] = {
        "id": book_id, "title": title, "borrowed": False
    }
    return jsonify(books[book_id]), 201


@app.post("/books/<int:book_id>/borrow")
def borrow_book(book_id):
    book = books.get(book_id)
    if book is None:
        return jsonify({"error": "book not found"}), 404
    if book["borrowed"]:
        return jsonify({"error": "book already borrowed"}), 409
    book["borrowed"] = True
    return jsonify(book)


@app.post("/books/<int:book_id>/return")
def return_book(book_id):
    book = books.get(book_id)
    if book is None:
        return jsonify({"error": "book not found"}), 404
    if not book["borrowed"]:
        return jsonify({"error": "book is not borrowed"}), 409

    book["borrowed"] = False
    return jsonify(book)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
