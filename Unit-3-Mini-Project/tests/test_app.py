from app import app

def test_home():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.json["status"] == "running"

def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_books():
    response = app.test_client().get("/books")
    assert response.status_code == 200
    assert len(response.json) >= 2

def test_add_book():
    response = app.test_client().post(
        "/books", json={"title": "Cloud Computing"}
    )
    assert response.status_code == 201
    assert response.json["title"] == "Cloud Computing"

def test_add_book_without_title():
    response = app.test_client().post("/books", json={})
    assert response.status_code == 400

def test_borrow_and_return_book():
    client = app.test_client()
    borrow_response = client.post("/books/1/borrow")
    assert borrow_response.status_code == 200
    return_response = client.post("/books/1/return")
    assert return_response.status_code == 200

def test_book_not_found():
    response = app.test_client().post("/books/9999/borrow")
    assert response.status_code == 404
