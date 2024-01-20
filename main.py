from fastapi import FastAPI

app = FastAPI(title="Learn FastAPI")

RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/recipe/{recipe_id}", status_code=200)
async def get_recipe(*, recipe_id: int = 0) -> dict:
    """ Get a single recipe by ID """
    
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    
    print(result)
    if result:
        return result[0]
    else:
        return {"message": "There is no recipes assigned with given id."}
    
