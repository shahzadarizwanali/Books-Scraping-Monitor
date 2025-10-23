# 📘 Book Scraper & Monitoring System (FastAPI + MongoDB)

A production-grade **Book Scraping and Monitoring API** built using **FastAPI**, **Async Python (httpx + asyncio)**, and **MongoDB**.  
This project crawls book data from [Books to Scrape](https://books.toscrape.com), stores it in MongoDB, and provides RESTful APIs to serve the data.

---

## 🧠 Problem Statement

Develop a scalable system that:

1. Crawls product data from an e-commerce site (`books.toscrape.com`).
2. Stores it in a NoSQL database (MongoDB).
3. Detects changes in data automatically via scheduling.
4. Exposes REST APIs with authentication, filtering, and pagination.

---

## ⚙️ Part 1 — Crawler (Robustness & Scalability)

### ✅ Implemented Features

- **Asynchronous crawling** using `httpx.AsyncClient` and `asyncio` for concurrency.
- Extracts complete **book details**:
  - Name, description, category
  - Price (including & excluding tax)
  - Availability, reviews, rating
  - Image URL, source URL, crawl timestamp
  - Raw HTML snapshot (fallback for verification)
- **Pagination** handled automatically (loops until no next page).
- **Data storage** in MongoDB (`book_scraper_db.books`) using `motor`.
- **Data export** to `scraped_data/books.csv` and `books.xlsx`.
- **Crawl metadata** (timestamp + source URL) stored with every record.

### 🔹 Pending Enhancements (Future Work)

- Implement **retry logic** with exponential backoff for failed requests.
- Support **resuming crawl** from the last successful page.
- Add **Pydantic Book schema** for data validation before insertion.
- Add **duplicate detection** using MongoDB index or hash field.
- Improve **structured logging** (replace print statements).

---

## ⏰ Part 2 — Scheduler & Change Detection

### ❌ Not Yet Implemented

The next phase will introduce a **daily scheduler** to detect data changes.

#### Planned Features

- Use **APScheduler or Celery** for periodic crawling.
- Compare latest crawl results to stored data:
  - Insert **new books**.
  - Update existing books when **price or availability** changes.
- Store updates in a **change_log** collection (with timestamps).
- Generate **daily reports** in JSON/CSV.
- Implement **hash/fingerprint comparison** to optimize change detection.
- Add **logging and email alerts** for significant changes.

---

## 🔐 Part 3 — RESTful API (FastAPI)

### ✅ Implemented Endpoints

| Endpoint   | Method | Description                                 |
| ---------- | ------ | ------------------------------------------- |
| `/`        | GET    | Health check endpoint                       |
| `/crawler` | POST   | Triggers asynchronous book scraping         |
| `/books`   | GET    | Fetches books with pagination (page, limit) |

### 🔹 Future API Improvements

- Add **filtering** (`category`, `min_price`, `max_price`, `rating`).
- Add **sorting** (by rating, price, or reviews).
- Add **GET /books/{book_id}** for book details.
- Add **GET /changes** for change logs.
- Implement **API key authentication** and **rate limiting** (100 req/hr).
- Add **Pydantic models** for request/response validation.
- Add **error handling middleware** for clean API responses.

---

## 🏗️ Project Architecture

```
BOOK_SCRAPER_PROJECT/
│
└── backend/
    ├── api/                  ← FastAPI app (main.py)
    ├── scraper/              ← Async crawler + MongoDB utils
    ├── scraped_data/         ← CSV/Excel outputs
    ├── requirements.txt      ← Dependencies
    ├── manage.py (Django)    ← (Optional admin interface)
    └── books_scraper/        ← Django settings (optional)
```

---

## 🧩 Technologies Used

| Category         | Technology                        |
| ---------------- | --------------------------------- |
| Language         | Python 3.10+                      |
| Framework        | FastAPI                           |
| Async Networking | httpx, asyncio                    |
| Database         | MongoDB (via `motor`)             |
| Data Parsing     | BeautifulSoup4                    |
| Data Export      | pandas + openpyxl                 |
| Task Scheduling  | (Planned) APScheduler / Celery    |
| Authentication   | (Planned) API key + rate limiting |
| Testing          | (Planned) pytest                  |

---

## 🧰 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/book-scraper.git
cd book-scraper/backend
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start MongoDB

Ensure MongoDB is running locally:

```bash
net start MongoDB
```

### 5️⃣ Run FastAPI Server

```bash
uvicorn api.main:app --reload
```

Open browser → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Testing via Postman

| Endpoint                 | Method | Example URL                                   |
| ------------------------ | ------ | --------------------------------------------- |
| `/`                      | GET    | `http://127.0.0.1:8000/`                      |
| `/crawler`               | POST   | `http://127.0.0.1:8000/crawler`               |
| `/books?page=1&limit=10` | GET    | `http://127.0.0.1:8000/books?page=1&limit=10` |

**Expected Response (`/crawler`)**

```json
{
  "status": "Crawler complete",
  "total_books": 1000,
  "csv_file": "scraped_data/books.csv",
  "excel_file": "scraped_data/books.xlsx"
}
```

---

## 🧱 Example MongoDB Document

```json
{
  "title": "A Light in the Attic",
  "description": "Beautiful poetry collection...",
  "category": "Poetry",
  "price_including_tax": "£51.77",
  "price_excluding_tax": "£49.25",
  "availability": "In stock",
  "num_reviews": "0",
  "rating": "Three",
  "image_url": "https://books.toscrape.com/...jpg",
  "page_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "crawl_timestamp": "2025-10-23 12:00:00",
  "raw_html": "<html>...</html>"
}
```

---

## 🧭 Current Status Summary

| Module                       | Status     | Notes                      |
| ---------------------------- | ---------- | -------------------------- |
| Async Web Crawler            | ✅ Done    | Core logic complete        |
| MongoDB Integration          | ✅ Done    | Using `motor` async driver |
| Pagination                   | ✅ Done    | Automatically handled      |
| CSV/Excel Export             | ✅ Done    | Via pandas                 |
| Scheduler & Change Detection | ❌ Pending | To be added                |
| Filtering, Sorting & Auth    | ❌ Pending | API enhancement phase      |
| Testing (pytest)             | ❌ Pending | For production readiness   |

✅ **Overall Completion:** ~60%  
Next target → implement **Part 2 (Scheduler + Change Detection)** and **API enhancements**.

---

## 👨‍💻 Author

**Shahzada Rizwan Ali**  
Python Developer (FastAPI | Django | Django Rest Framework)  
📧 shahzadarizwanali01@gmail.com  
🌐 [GitHub](https://github.com/shahzadarizwanali)

---

## 🏁 License

This project is open-source under the **MIT License**.
