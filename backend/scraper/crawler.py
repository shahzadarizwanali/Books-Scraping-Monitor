import httpx
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://books.toscrape.com/"


async def fetch_page(client, url):
    try:
        resp = await client.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def scrape_books():
    books_list = []
    page_num = 1

    async with httpx.AsyncClient() as client:
        while True:
            url = BASE_URL + f"catalogue/page-{page_num}.html"
            html = await fetch_page(client, url)
            if not html:
                break

            soup = BeautifulSoup(html, "html.parser")
            books = soup.select("article.product_pod")
            if not books:
                break

            tasks = []
            for book in books:
                page_url = (
                    BASE_URL + "catalogue/" + book.h3.a["href"].replace("../", "")
                )
                tasks.append(fetch_page(client, page_url))

            detail_pages = await asyncio.gather(*tasks)

            for book, detail_html in zip(books, detail_pages):
                if not detail_html:
                    continue

                title = book.h3.a["title"]
                image_url = BASE_URL + book.img["src"].replace("../", "")
                classes = book.p.get("class", [])
                rating = classes[1] if len(classes) > 1 else "No rating"

                detail_soup = BeautifulSoup(detail_html, "html.parser")

                description_tag = detail_soup.select_one("#product_description ~ p")
                description = description_tag.text.strip() if description_tag else ""

                category_tag = detail_soup.select("ul.breadcrumb li a")
                category = category_tag[2].text.strip() if len(category_tag) > 2 else ""

                def extract(th_str):
                    tag = detail_soup.find("th", string=th_str)
                    return tag.find_next_sibling("td").text.strip() if tag else ""

                price_incl_tax = extract("Price (incl. tax)")
                price_excl_tax = extract("Price (excl. tax)")
                availability = extract("Availability")
                num_reviews = extract("Number of reviews") or "0"

                crawl_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                books_list.append(
                    {
                        "title": title,
                        "description": description,
                        "category": category,
                        "price_including_tax": price_incl_tax,
                        "price_excluding_tax": price_excl_tax,
                        "availability": availability,
                        "num_reviews": num_reviews,
                        "image_url": image_url,
                        "rating": rating,
                        "page_url": page_url,
                        "crawl_timestamp": crawl_timestamp,
                        "raw_html": detail_html,
                    }
                )

            page_num += 1

    return books_list
