import pandas as pd
import os
import motor.motor_asyncio

MONGO_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["book_scraper_db"]
collection = db["books"]


async def save_books_mongo(books):
    if books:
        await collection.insert_many(books)
    return len(books)


def save_books_csv_excel(books, data_dir):
    os.makedirs(data_dir, exist_ok=True)
    df = pd.DataFrame(books)
    csv_file = os.path.join(data_dir, "books.csv")
    excel_file = os.path.join(data_dir, "books.xlsx")
    df.to_csv(csv_file, index=False, encoding="utf-8")
    df.to_excel(excel_file, index=False, engine="openpyxl")
    return csv_file, excel_file
