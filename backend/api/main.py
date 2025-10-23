from fastapi import FastAPI
from scraper.crawler import scrape_books
from scraper.utils import save_books_csv_excel, save_books_mongo
import os

app = FastAPI(title="Book Scraper API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../scraped_data")
os.makedirs(DATA_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"Hello This is Home"}


@app.post("/crawler")
async def run_crawler():
    books = await scrape_books()
    if books:
        mongo_count = await save_books_mongo(books)

        csv_file, excel_file = save_books_csv_excel(books, DATA_DIR)

        return {
            "status": "Crawler complete",
            "total_books": mongo_count,
            "csv_file": csv_file,
            "excel_file": excel_file,
        }
    return {"status": "No books scraped"}


@app.get("/books")
async def get_books(page: int = 1, limit: int = 10):
    from scraper.utils import collection

    skip = (page - 1) * limit

    cursor = collection.find().skip(skip).limit(limit)
    books = await cursor.to_list(length=limit)

    total_books = await collection.count_documents({})

    return {"page": page, "limit": limit, "total_books": total_books, "books": books}
