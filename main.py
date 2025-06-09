from fastapi import FastAPI
from scrapers.multistore import scrape_all_categories

app = FastAPI()

@app.get("/products")
async def get_all_products():
    return await scrape_all_categories()
