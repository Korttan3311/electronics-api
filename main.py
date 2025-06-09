from fastapi import FastAPI
from scrapers.courts import scrape_courts

app = FastAPI()

@app.get("/products/courts")
async def get_courts():
    return await scrape_courts()
