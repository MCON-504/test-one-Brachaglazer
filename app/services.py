from sqlalchemy import desc

from .extensions import db
from .models import Recipe


def get_all_recipes() -> list[dict]:
    """Return a list of all recipes ordered by newest first.

    Steps:
        1. Query all Recipe records, ordered by created_at descending.
        2. Convert each Recipe to a dict using its to_dict() method.
        3. Return the list of dicts.
    """
    # TODO: Implement this method
    recipes = Recipe.query.order_by(Recipe.created_at, desc).all()
    recipes_list = []
    for recipe in recipes:
        recipes_list.append(recipe.to_dict())
    return recipes_list

def get_recipe_by_id(recipe_id: int) -> dict:
    """Return a single recipe dict by its id, or 404.

    Steps:
        1. Use query.get_or_404() to fetch the Recipe.
        2. Return the recipe as a dict.
    """
    # TODO: Implement this method
    recipe = db.session.query.get_or_404(Recipe, recipe_id).first()
    return recipe.to_dict()


def create_recipe(data: dict) -> dict:
    """Create a new Recipe from the provided data dict and return it.

    The data dict will contain: title, description, instructions, prep_time, user_id.

    Steps:
        1. Create a new Recipe instance using values from `data`.
        2. Add it to the database session and commit.
        3. Return the new recipe as a dict.
    """
    # TODO: Implement this method
    recipe = Recipe(title=data["title"], description=data["description"], instructions=data["instructions"], prep_time=data["prep_time"], user_id=data["user_id"])
    db.session.add(recipe)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "there was an error saving your recipe."}
    return recipe.to_dict()


def delete_recipe(recipe_id: int) -> None:
    """Delete a recipe by its id, or 404 if not found.

    Steps:
        1. Fetch the Recipe by id (404 if missing).
        2. Delete it from the session and commit.
    """
    # TODO: Implement this method
    recipe = db.session.query.get_or_404(Recipe, recipe_id).first()
    db.session.delete(recipe)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        #return {"error": "there was an error deleting your recipe."}
    #return {"success": "your recipe has been deleted"}
    #return {}, 204


def update_recipe(recipe_id: int, data: dict) -> dict:
    """Update an existing recipe with the provided data and return it.

    The data dict may contain any of: title, description, instructions, prep_time.

    Steps:
        1. Fetch the Recipe by id (404 if missing).
        2. Update only the fields present in `data`.
        3. Commit the changes.
        4. Return the updated recipe as a dict.
    """
    # TODO: Implement this method
    recipe = db.session.get_or_404(Recipe, recipe_id)
    if "title" in data:
        recipe.title = data["title"]
    if "description" in data:
        recipe.description = data["description"]
    if "instructions" in data:
        recipe.instructions = data["instructions"]
    if "prep_time" in data:
        recipe.prep_time = data["prep_time"]
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "error updating your recipe"}
    return recipe.to_dict()


