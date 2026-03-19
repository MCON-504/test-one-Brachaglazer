import pytest

from app import create_app
from app.extensions import db
from app.models import User, Recipe


@pytest.fixture()
def app():
    """Create a test app with an in-memory SQLite database."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

        # seed a user and a recipe for tests
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()

        recipe = Recipe(
            title="Seed Recipe",
            description="A seeded recipe.",
            instructions="Step 1. Step 2.",
            prep_time=15,
            user_id=user.id,
        )
        db.session.add(recipe)
        db.session.commit()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


# ------------------------------------------------------------------ #
#  GET /api/recipes
# ------------------------------------------------------------------ #

class TestGetAllRecipes:
    def test_returns_200(self, client):
        resp = client.get("/api/recipes")
        assert resp.status_code == 200

    def test_returns_list(self, client):
        resp = client.get("/api/recipes")
        data = resp.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_recipe_has_expected_fields(self, client):
        resp = client.get("/api/recipes")
        recipe = resp.get_json()[0]
        for field in ("id", "title", "description", "instructions", "prep_time", "created_at", "user_id"):
            assert field in recipe


# ------------------------------------------------------------------ #
#  GET /api/recipes/<id>
# ------------------------------------------------------------------ #

class TestGetRecipeById:
    def test_returns_200_for_existing(self, client):
        resp = client.get("/api/recipes/1")
        assert resp.status_code == 200

    def test_returns_correct_recipe(self, client):
        resp = client.get("/api/recipes/1")
        data = resp.get_json()
        assert data["id"] == 1
        assert data["title"] == "Seed Recipe"

    def test_returns_404_for_missing(self, client):
        resp = client.get("/api/recipes/9999")
        assert resp.status_code == 404


# ------------------------------------------------------------------ #
#  POST /api/recipes
# ------------------------------------------------------------------ #

class TestCreateRecipe:
    def _valid_payload(self):
        return {
            "title": "New Recipe",
            "description": "Desc",
            "instructions": "Do stuff",
            "prep_time": 20,
            "user_id": 1,
        }

    def test_returns_201(self, client):
        resp = client.post("/api/recipes", json=self._valid_payload())
        assert resp.status_code == 201

    def test_returns_created_recipe(self, client):
        resp = client.post("/api/recipes", json=self._valid_payload())
        data = resp.get_json()
        assert data["title"] == "New Recipe"
        assert "id" in data

    def test_missing_fields_returns_400(self, client):
        resp = client.post("/api/recipes", json={"title": "Incomplete"})
        assert resp.status_code == 400


# ------------------------------------------------------------------ #
#  PUT /api/recipes/<id>
# ------------------------------------------------------------------ #

class TestUpdateRecipe:
    def test_returns_200(self, client):
        resp = client.put("/api/recipes/1", json={"title": "Updated Title"})
        assert resp.status_code == 200

    def test_updates_fields(self, client):
        client.put("/api/recipes/1", json={"title": "Updated Title", "prep_time": 99})
        resp = client.get("/api/recipes/1")
        data = resp.get_json()
        assert data["title"] == "Updated Title"
        assert data["prep_time"] == 99

    def test_returns_404_for_missing(self, client):
        resp = client.put("/api/recipes/9999", json={"title": "Nope"})
        assert resp.status_code == 404


# ------------------------------------------------------------------ #
#  DELETE /api/recipes/<id>
# ------------------------------------------------------------------ #

class TestDeleteRecipe:
    def test_returns_204(self, client):
        resp = client.delete("/api/recipes/1")
        assert resp.status_code == 204

    def test_body_is_empty(self, client):
        resp = client.delete("/api/recipes/1")
        assert resp.data == b""

    def test_recipe_is_gone_after_delete(self, client):
        client.delete("/api/recipes/1")
        resp = client.get("/api/recipes/1")
        assert resp.status_code == 404

    def test_returns_404_for_missing(self, client):
        resp = client.delete("/api/recipes/9999")
        assert resp.status_code == 404

